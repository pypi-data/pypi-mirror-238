from dataclasses import dataclass
from typing import Any, Union


@dataclass
class Scalar:
    timestamp: float
    value: float

    @classmethod
    def from_data(cls, data: tuple[float, float]) -> 'Scalar':
        return cls(
            timestamp=data[0],
            value=float(data[1])
        )


@dataclass
class InstantSeries:
    metric: dict[str, str]
    value: Scalar

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> 'InstantSeries':
        return cls(
            metric=data['metric'],
            value=Scalar.from_data(data['value'])
        )


@dataclass
class InstantVector:
    series: list[InstantSeries]

    @classmethod
    def from_data(cls, data: list[dict[str, Any]]) -> 'InstantVector':
        return cls(
            series=[
                InstantSeries.from_data(i)
                for i in data
            ]
        )


@dataclass
class RangeSeries:
    metric: dict[str, str]
    values: list[Scalar]

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> 'RangeSeries':
        return cls(
            metric=data['metric'],
            values=[
                Scalar.from_data(i)
                for i in data['values']
            ]
        )


@dataclass
class RangeVector:
    series: list[RangeSeries]

    @classmethod
    def from_data(cls, data: list[dict[str, Any]]) -> 'RangeVector':
        return cls(
            series=[
                RangeSeries.from_data(i)
                for i in data
            ]
        )


def parse_data(
    data: dict[str, Any]
) -> Union[Scalar, InstantVector]:
    result_type = data['resultType']
    result = data['result']

    if result_type == 'scalar':
        return Scalar.from_data(result)
    elif result_type == 'vector':
        return InstantVector.from_data(result)

    raise ValueError('unexpected result type: %s' % result_type)
