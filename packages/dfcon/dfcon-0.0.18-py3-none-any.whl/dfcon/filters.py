"""Implement Basic Filter Class"""

from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import List, Optional


class Filter(metaclass=ABCMeta):
    """Basic Filter Class"""

    @abstractmethod
    def __call__(self, target: object) -> bool:
        raise NotImplementedError()

    @staticmethod
    def tile(filters: List[Filter] | Filter) -> TiledFilter:
        """Generate TiledFilter instance with `filters`.

        Args:
            filters (List[Filter] | Filter)

        Returns:
            TiledFilter: Compound filter consisting of a fFilter joined by the OR operator.
        """

        if isinstance(filters, Filter):
            filters = [filters]
        elif not isinstance(filters, list):
            raise TypeError(
                "The argument 'filters' type must be 'Filter' or 'List[Filter]', "
                + f"but detect '{filters.__class__.__name__}'",
            )
        elif filters == []:
            return TiledFilter(None)
        elif not isinstance(filters[0], Filter):
            raise TypeError(
                "The argument 'filters' type must be 'Filter' or 'List[Filter]', "
                + f"but detect '{filters.__class__.__name__}'",
            )
        return TiledFilter(filters)

    @staticmethod
    def overlap(filters: List[Filter] | Filter) -> OverlapedFilter:
        """Generate OverlapedFilter instance with `filters`.

        Args:
            filters (List[Filter] | Filter)

        Returns:
            OverlapedFilter: Compound filter consisting of a fFilter joined by the AND operator.
        """

        if isinstance(filters, Filter):
            filters = [filters]
        elif not isinstance(filters, list):
            raise TypeError(
                "The argument 'filters' type must be 'Filter' or 'List[Filter]', "
                + f"but detect '{filters.__class__.__name__}'",
            )
        elif filters == []:
            return OverlapedFilter(None)
        elif not isinstance(filters[0], Filter):
            raise TypeError(
                "The argument 'filters' type must be 'Filter' or 'List[Filter]', "
                + f"but detect '{filters.__class__.__name__}'",
            )
        return OverlapedFilter(filters)

    def __or__(self, other: Filter) -> TiledFilter:
        return TiledFilter([self, other])

    def __and__(self, other: Filter) -> OverlapedFilter:
        return OverlapedFilter([self, other])


class TiledFilter(Filter):
    """Compound filter consisting of a Filter joined by the OR operator."""

    def __init__(self, filters: Optional[List[Filter]]) -> None:
        super().__init__()
        self.filters = filters if filters is not None else []

    def __call__(self, target: object) -> bool:
        for _f in self.filters:
            if _f(target=target):
                return True
        return False


class OverlapedFilter(Filter):
    """Compound filter consisting of a Filter joined by the AND operator."""

    def __init__(self, filters: Optional[List[Filter]]) -> None:
        super().__init__()
        self.filters = filters if filters is not None else []

    def __call__(self, target: object) -> bool:
        for _f in self.filters:
            if not _f(target=target):
                return False
        return True


class EmpFilter(Filter):
    """Empty Filter"""

    def __call__(self, target: object) -> bool:
        return True
