import aiohttp
from pg_common import log_info


__all__ = ["get_text", "get_json", 'post_text', 'post_json']
__auth__ = "baozilaji@gmail.com"


async def _http(url, r_type="json", m_type="get", **kwargs):
    log_info(f"{m_type}: {url}, param: {kwargs}")
    async with aiohttp.ClientSession() as session:
        async with getattr(session, m_type)(url, **kwargs) as res:
            _ret = None
            if r_type == "json":
                _ret = await res.json()
            else:
                _ret = await res.text()
            log_info(f"ret, {r_type}, {_ret}")
            return _ret

async def get_text(url, **kwargs):
    return await _http(url, r_type="text", m_type="get", **kwargs)


async def get_json(url, **kwargs):
    return await _http(url, r_type="json", m_type="get", **kwargs)


async def post_text(url, **kwargs):
    return await _http(url, r_type="text", m_type="post", **kwargs)


async def post_json(url, **kwargs):
    return await _http(url, r_type="json", m_type="post", **kwargs)
