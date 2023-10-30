from time import time as get_current_timestamp
from urllib.parse import urljoin
from typing import Optional, Any, Union, TypedDict

import httpx

from . import errors
from .model import parse_data, InstantVector, Scalar, RangeVector

DEFAULT_USER_AGENT = 'Python Aio Prometheus Client'
TIMEOUT = 10 * 60


class PromJsonData(TypedDict):
    status: str
    data: dict[str, Any]


class PrometheusClient:
    base_url: str
    user_agent: str

    def __init__(self, base_url: str, user_agent: str = DEFAULT_USER_AGENT):
        self.base_url = base_url
        self.user_agent = user_agent

    async def _request(
        self,
        path: str,
        params: Optional[dict[str, Union[str, int, float]]] = None
    ) -> dict[str, Any]:
        data: PromJsonData

        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(
                    urljoin(self.base_url, path),
                    params=params,
                    headers={'User-Agent': self.user_agent},
                    timeout=TIMEOUT,
                )
            except Exception as e:
                raise errors.PrometheusConnectionError('request fail') from e

            if r.status_code == 400:
                err_data = r.json()
                raise errors.PrometheusMeticError(r.status_code, err_data)

            r.raise_for_status()
            data = r.json()

        if data['status'] != 'success':
            raise ValueError('invalid data: %s' % data)

        return data['data']

    async def query(
        self, metric: str, time: float = 0
    ) -> Union[Scalar, InstantVector]:
        if not time:
            time = get_current_timestamp()

        data: dict[str, Any] = await self._request(
            path='api/v1/query',
            params={
                'query': metric,
                'time': str(time)
            }
        )

        return parse_data(data)

    async def query_value(self, metric: str) -> float:
        data = await self.query(metric)
        if isinstance(data, InstantVector):
            series_count = len(data.series)
            if series_count != 1:
                raise ValueError('series count incorrect: %d' % series_count)

            return data.series[0].value.value
        elif isinstance(data, Scalar):
            return data.value
        else:
            raise TypeError('unknown data type: %s' % type(data))

    async def query_range(
        self, metric: str, start: float, end: float,
        step: Optional[float] = None, step_count: int = 60
    ) -> RangeVector:
        if step is None:
            if start >= end:
                raise ValueError('end must be greater than start')

            step = (end - start) / step_count
            if step < 1:
                step = 1
            else:
                step = int(step)

        data: dict[str, Any] = await self._request(
            path='api/v1/query_range',
            params={
                'query': metric,
                'start': start,
                'end': end,
                'step': step,
            }
        )

        result_type = data['resultType']
        result = data['result']

        if result_type != 'matrix':
            raise ValueError('unexpected result type: %s' % result_type)

        return RangeVector.from_data(result)
