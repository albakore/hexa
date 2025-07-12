from dataclasses import dataclass
from typing import Any

import httpx
from httpx._types import AuthTypes, CookieTypes, HeaderTypes, QueryParamTypes, RequestContent, RequestData, RequestFiles, TimeoutTypes


@dataclass
class YiqiHttpClient:
	base_url: str
	api_key: str
	api_timeout: float = 30.0
	
	def __post_init__(self):
		self._client = httpx.AsyncClient(
			base_url=self.base_url,
			headers={"Authorization": f"Bearer {self.api_key}"},
			timeout=self.api_timeout
		)

	def _extract_content_type_header(self, response : httpx.Response) -> str:
		content_type = response.headers.get("Content-Type","application/json")
		return content_type


	async def get(self,
		path: str,
		params: QueryParamTypes | None = None,
		headers: HeaderTypes | None = None,
		cookies: CookieTypes | None = None,
		auth: AuthTypes | None = None,
		timeout: TimeoutTypes | None=None,

		):

		if not auth:
			auth = self._client.auth
		if not timeout:
			timeout = self._client.timeout

		response = await self._client.get(
			path,
			params=params,
			headers=headers,
			cookies=cookies,
			timeout=timeout
		)
		setattr(response,"content_type",self._extract_content_type_header(response))
		return response

	async def post(self,
		path: str,
		content: RequestContent | None = None,
		data: RequestData | None = None,
		files: RequestFiles | None = None,
		json: Any | None = None,
		params: QueryParamTypes | None = None,
		headers: HeaderTypes | None = None,
		cookies: CookieTypes | None = None,
		timeout: TimeoutTypes | None=None,
		):
		if not timeout:
			timeout = self._client.timeout

		response = await self._client.post(
			path,
			content=content,
			data=data,
			files=files,
			json=json,
			params=params,
			headers=headers,
			cookies=cookies,
			timeout=timeout
		)
		setattr(response,"content_type",self._extract_content_type_header(response))
		return response

	async def close(self):
		await self._client.aclose()