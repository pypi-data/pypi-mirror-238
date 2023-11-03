from _typeshed import Incomplete
from amsdal_models.classes.model import Model as Model
from amsdal_models.querysets.errors import MultipleObjectsReturnedError as MultipleObjectsReturnedError, ObjectDoesNotExistError as ObjectDoesNotExistError
from amsdal_models.querysets.executor import DEFAULT_DB_ALIAS as DEFAULT_DB_ALIAS, Executor as Executor
from amsdal_utils.query.utils import Q
from typing import Any, Optional, TypeVar

logger: Incomplete
QuerySetType = TypeVar('QuerySetType', bound='QuerySetBase')

class QuerySetBase:
    """
    Base class for QuerySets.
    """
    def __init__(self, entity: type['Model']) -> None: ...
    @property
    def entity_name(self) -> str: ...
    def using(self, value: str) -> QuerySetType: ...
    def __copy__(self) -> QuerySetType: ...
    def only(self, fields: list[str]) -> QuerySetType:
        """
        Limit the number of fields to be returned.


        :param fields: the fields to be returned
        :type fields: list[str]

        :rtype: QuerySetType
        """
    def distinct(self, fields: list[str]) -> QuerySetType:
        """
        Return only distinct (different) values.

        :param fields: the fields to be distinct
        :type fields: list[str]

        :rtype: QuerySetType
        """
    def filter(self, *args: Q, **kwargs: Any) -> QuerySetType:
        """
        Apply filters to the query. The filters are combined with AND.

        :param args: the filters to be applied
        :type args: Q
        :param kwargs: the filters to be applied
        :type kwargs: Any

        :rtype: QuerySetType
        """
    def exclude(self, *args: Q, **kwargs: Any) -> QuerySetType:
        """
        Exclude filters from the query. The filters are combined with AND.

        :param args: the filters to be applied
        :type args: Q
        :param kwargs: the filters to be applied
        :type kwargs: Any

        :rtype: QuerySetType
        """
    def order_by(self, *args: str) -> QuerySetType:
        """
        Order the query by the given fields.

        :param args: the fields to order by
        :type args: str

        :rtype: QuerySetType
        """
    def __getitem__(self, index: slice | int) -> QuerySetType: ...

class QuerySet(QuerySetBase):
    """
    Interface to access the database.
    """
    def get(self, *args: Q, **kwargs: Any) -> QuerySetOneRequired:
        """
        Change the QuerySet to a QuerySetOneRequired. Query execution will return a single item or raise an error.

        :param args: the filters to be applied
        :type args: Q
        :param kwargs: the filters to be applied
        :type kwargs: Any

        :rtype: QuerySetOneRequired
        """
    def get_or_none(self, *args: Q, **kwargs: Any) -> QuerySetOne:
        """
        Change the QuerySet to a QuerySetOne. Query execution will return a single item or None.

        :param args: the filters to be applied
        :type args: Q
        :param kwargs: the filters to be applied
        :type kwargs: Any

        :rtype: QuerySetOneRequired
        """
    def first(self, *args: Q, **kwargs: Any) -> QuerySetOne:
        """
        Change the QuerySet to a QuerySetOne. Query execution will return the first item or None.

        :param args: the filters to be applied
        :type args: Q
        :param kwargs: the filters to be applied
        :type kwargs: Any

        :rtype: QuerySetOneRequired
        """
    def count(self) -> QuerySetCount:
        """
        Change the QuerySet to a QuerySetCount. Query execution will return the count of items.
        """
    def execute(self) -> list['Model']:
        """
        Return the list of items.

        :rtype: list[Model]
        """

class QuerySetOne(QuerySetBase):
    """
    QuerySet class for models. QuerySet is executed to a single model object or None.
    """
    def __init__(self, entity: type['Model']) -> None: ...
    def execute(self) -> Optional['Model']:
        """
        Query the database and return the single item or None.

        :raises MultipleObjectsReturnedError: If multiple items are found.

        :rtype: Model | None
        """

class QuerySetOneRequired(QuerySetOne):
    """
    QuerySet class for models. QuerySet is executed to a single model object or raises an error.
    """
    def execute(self) -> Model:
        """
        Return the single item.

        :raises ObjectDoesNotExistError: If no items are found.

        :rtype: Model

        """

class QuerySetCount(QuerySetBase):
    """
    QuerySet class for models. QuerySet is executed to a count of items.
    """
    def execute(self) -> int:
        """
        Return the count of items.

        :rtype: int
        """
