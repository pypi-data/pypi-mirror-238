import logging
import re
from typing import Dict, List, Optional, Tuple, Union

from lxml.html import HtmlElement, document_fromstring
from tenacity import after_log, retry, stop_after_attempt

from aioqzone.api.login import Loginable
from aioqzone.exception import QzoneError
from aioqzone.utils.regex import entire_closing, response_callback
from aioqzone.utils.retry import retry_if_qzone_code, retry_if_status
from qqqr.utils.iter import firstn
from qqqr.utils.jsjson import JsonValue, json_loads
from qqqr.utils.net import ClientAdapter

StrDict = Dict[str, JsonValue]


log = logging.getLogger(__name__)


class QzoneH5RawAPI:
    host = "https://h5.qzone.qq.com"
    qzonetoken: str = ""

    def __init__(
        self, client: ClientAdapter, loginman: Loginable, *, retry_if_login_expire: bool = True
    ) -> None:
        """
        .. warning:: If `loginman` uses an `AsyncClient`, the `client` param MUST use this client as well.
        """
        super().__init__()
        self.client = client
        self.login = loginman
        self._relogin_retry = retry(
            stop=stop_after_attempt(2 if retry_if_login_expire else 1),
            retry=retry_if_status(302, 403) | retry_if_qzone_code(-3000, -10000),
            after=after_log(log, logging.INFO),
            sleep=self._update_cookie_safe,
        )
        """A decorator which will relogin and retry given func if cookie expired.

        'cookie expired' is indicated by:

        - `aioqzone.exception.QzoneError` code -3000/-10000
        - HTTP response code 302/403

        :meta public:

        .. note:: Decorate code as less as possible
        .. warning::

                You *SHOULD* **NOT** wrap a function with mutable input. If you change the mutable
                var in the first attempt, in the second attempt the var saves the changed value.
        """

    def host_get(
        self,
        path: str,
        params: Optional[dict] = None,
        *,
        attach_token=True,
        host: Optional[str] = None,
        **kw,
    ):
        params = {} if params is None else params.copy()
        if "p_skey" not in self.login.cookie:
            raise QzoneError(-3000, "未登录")
        if attach_token:
            params["qzonetoken"] = self.qzonetoken
            params["g_tk"] = str(self.login.gtk)
            self.client.referer = "https://h5.qzone.qq.com/"
        host = host or self.host
        return self.client.get(host + path, params=params, cookies=self.login.cookie, **kw)

    def host_post(
        self,
        path: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        *,
        attach_token=True,
        host: Optional[str] = None,
        **kw,
    ):
        params = {} if params is None else params.copy()
        if "p_skey" not in self.login.cookie:
            raise QzoneError(-3000, "未登录")
        if attach_token:
            params["qzonetoken"] = self.qzonetoken
            params["g_tk"] = str(self.login.gtk)
        self.client.referer = "https://h5.qzone.qq.com/"
        host = host or self.host
        return self.client.post(
            self.host + path, params=params, data=data, cookies=self.login.cookie, **kw
        )

    async def _update_cookie_safe(self, *_) -> None:
        await self.login.new_cookie()

    def _rtext_handler(
        self,
        robj: Union[str, StrDict],
        cb: bool = True,
        errno_key: Tuple[str, ...] = ("code", "err"),
        msg_key: Tuple[str, ...] = ("message", "msg"),
        data_key: Optional[str] = None,
    ) -> StrDict:
        """Handles the response text recieved from Qzone API, returns the parsed json dict.

        :meta public:
        :param rtext: response text
        :param cb: The text is to be parsed by callback_regex, defaults to True.
        :param errno_key: Error # key, defaults to ('code', 'err').
        :param msg_key: Error message key, defaults to ('msg', 'message').

        :raise `aioqzone.exception.QzoneError`: if errno != 0

        :return: json response
        """
        if isinstance(robj, str):
            if cb:
                match = response_callback.search(robj)
                assert match
                robj = str(match.group(1))
            r = json_loads(robj)
        else:
            r = robj

        assert isinstance(r, dict)

        err = firstn((r.get(i) for i in errno_key), lambda i: i is not None)
        assert err is not None, f"no {errno_key} in {r.keys()}"
        assert isinstance(err, (int, str))
        err = int(err)

        if err != 0:
            msg = firstn((r.get(i) for i in msg_key), lambda i: i is not None)
            if msg:
                raise QzoneError(err, msg, rdict=r)
            else:
                raise QzoneError(err, rdict=r)

        return r[data_key] if data_key is not None else r  # type: ignore

    async def index(self) -> StrDict:
        """This api is the redirect page after h5 login, which is also the landing (main) page of h5 qzone.

        :raise `RuntimeError`: if any failure occurs in data parsing.
        """

        @self._relogin_retry
        async def retry_closure():
            async with self.host_get("/mqzone/index", attach_token=False) as r:
                r.raise_for_status()

                html = await r.text()
                scripts: List[HtmlElement] = document_fromstring(html).xpath(
                    'body/script[@type="application/javascript"]'
                )
                if not scripts:
                    log.debug("jump to %s", str(r.url))
                    log.debug(f"request header cookies: {r.request_info.headers['Cookie']}")
                    log.debug(f"loginman cookies: {self.login.cookie}")
                    raise QzoneError(-3000, "script tag not found")

                texts: List[str] = [s.text for s in scripts]
                script = firstn(texts, lambda s: "shine0callback" in s)
                if not script:
                    raise QzoneError(-3000, "data script not found")

                m = re.search(r'window\.shine0callback.*return "([0-9a-f]+?)";', script)
                if m is None:
                    raise RuntimeError("data script not found")

                self.qzonetoken = m.group(1)
                log.debug(f"got qzonetoken = {self.qzonetoken}")

                m = re.search(r"var FrontPage =.*?data\s*:\s*\{", script)
                if m is None:
                    raise RuntimeError("page data not found")
                data = script[m.end() - 1 : m.end() + entire_closing(script[m.end() - 1 :])]
                return self._rtext_handler(
                    data, cb=False, errno_key=("code", "ret"), data_key="data"
                )

        return await retry_closure()

    async def get_active_feeds(self, attach_info: str) -> StrDict:
        """Get next page. If :obj:`.qzonetoken` is not parsed or :obj:`attach_info` is empty,
        it will call :meth:`.index` and return its response.

        :param attach_info: The ``attach_info`` field from last call.
            Pass an empty string equals to call :meth:`.index`.
        :return: If success, the ``data`` field of the response.
        """
        if not self.qzonetoken or not attach_info:
            return await self.index()

        data = dict(
            res_type=0,
            res_attach=attach_info,
            refresh_type=2,
            format="json",
            attach_info=attach_info,
        )
        log.debug("get_active_feeds post data:", data)

        @self._relogin_retry
        async def retry_closure() -> StrDict:
            async with self.host_post("/webapp/json/mqzone_feeds/getActiveFeeds", data=data) as r:
                r.raise_for_status()
                return self._rtext_handler(
                    await r.json(), cb=False, errno_key=("code", "ret"), data_key="data"
                )

        return await retry_closure()

    async def shuoshuo(self, fid: str, hostuin: int, appid=311, busi_param: str = ""):
        """This can be used to get the detailed summary of a feed.

        :param fid: aka. ``cellid``
        :param hostuin: uin of the owner of the given feed
        :param appid: appid of the given feed, default as 311
        :param busi_param: optional encoded params
        """
        data = dict(
            format="json",
            appid=appid,
            uin=hostuin,
            count=20,
            refresh_type=31,
            cellid=fid,
            subid="",
        )
        if busi_param and len(busi_param) < 100:
            data["busi_param"] = busi_param

        @self._relogin_retry
        async def retry_closure() -> StrDict:
            async with self.host_get("/webapp/json/mqzone_detail/shuoshuo", data) as r:
                r.raise_for_status()
                return self._rtext_handler(await r.json(), cb=False, data_key="data")

        return await retry_closure()

    async def mfeeds_get_count(self) -> StrDict:
        @self._relogin_retry
        async def retry_closure() -> StrDict:
            async with self.host_get(
                "/feeds/mfeeds_get_count", dict(format="json"), host="https://mobile.qzone.qq.com"
            ) as r:
                r.raise_for_status()
                return self._rtext_handler(
                    await r.json(content_type=None), cb=False, data_key="data"
                )

        return await retry_closure()

    async def internal_dolike_app(
        self, appid: int, unikey: str, curkey: str, like=True
    ) -> StrDict:
        data = dict(
            opuin=self.login.uin,
            unikey=unikey,
            curkey=curkey,
            appid=appid,
            opr_type="like",
            format="purejson",
        )
        if like:
            path = "/proxy/domain/w.qzone.qq.com/cgi-bin/likes/internal_dolike_app"
        else:
            path = "/proxy/domain/w.qzone.qq.com/cgi-bin/likes/internal_unlike_app"

        @self._relogin_retry
        async def retry_closure() -> StrDict:
            async with self.host_get(path, data) as r:
                r.raise_for_status()
                return self._rtext_handler(await r.json(), errno_key=("ret",), cb=False)

        return await retry_closure()

    async def add_comment(self, ownuin: int, srcId: str, appid: int, content: str, private=False):
        assert content, "comment should not be empty"
        assert len(content) <= 2000, "comment maxlen=2000"

        data = dict(
            ownuin=str(ownuin),
            srcId=srcId,
            uin=self.login.uin,
            isPrivateComment=int(private),
            content=content,
            appid=appid,
            bypass_param={},
            busi_param={},
        )
        log.debug("add_comment post data:", data)

        @self._relogin_retry
        async def retry_closure() -> StrDict:
            async with self.host_post("/webapp/json/qzoneOperation/addComment", data=data) as r:
                r.raise_for_status()
                return self._rtext_handler(
                    await r.json(), cb=False, errno_key=("ret",), data_key="data"
                )

        return await retry_closure()
