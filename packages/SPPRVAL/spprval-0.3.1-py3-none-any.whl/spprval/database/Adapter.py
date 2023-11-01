from typing import Generator
import pandas as pd


class DBAdapter:
    # name level constants
    GRANULARY: dict[str, str] = {}
    PROCESSED: dict[str, str] = {}
    TYPEDLVL2: dict[str, str] = {}

    def __init__(self, *args, **kwargs):
        """

        Args:
            connect: connect object for database.
                     can be a reference to a database service, as well as a sql connect object or None

        """
        raise NotImplementedError

    def from_names(
        self,
        works: list[str],
        resources: list[str] = (),
        ceil_limit: int = 1_000,
        objects_limit: int = 1,
        crossing: bool = False,
        key: dict[str, str] = GRANULARY,
        res_key: dict[str, str] = GRANULARY,
        *args,
        **kwargs,
    ) -> Generator[pd.DataFrame, None, None]:
        """
        Returns all schedules that include jobs and resources from the lists

        Args:
            works: list of works for which schedules are searched
            resources: list of resources for which schedules are searched
            ceil_limit: limit of records for one-time issuance from the database
            objects_limit: limit of objects for one-time issuance from the database
            crossing: flag describing the logic of combining resources and activities.
                      true - select schedules than contain work AND resources
                      false - select schedules than contain work OR resources
            key: level of works names
            res_key: level of resources names

        Returns:
            Pandas dataframe generator
        """
        raise NotImplementedError

    def get_works_by_pulls(
        self,
        work_pulls: list[list[str]],
        resource_list: list[list[str]] = [],
        key: dict[str, str] = GRANULARY,
        res_key: dict[str, str] = GRANULARY,
        *args,
        **kwargs,
    ) -> Generator[pd.DataFrame, None, None]:
        """
        Generator
        Returns information about work pools

        Args:
            work_pulls: list of works pulls
            resource_list: list of resources using on pulls
            key: level of works names
            res_key: level of resources names

        Returns:
            Pandas dataframe generator
        """
        raise NotImplementedError

    def get_all_works_name(self, *args, **kwargs) -> pd.DataFrame:
        """
        Returns all works names

        Returns:
            pandas dataframe
        """
        raise NotImplementedError

    def get_all_resources_name(self, *args, **kwargs) -> pd.DataFrame:
        """
        Returns all resources names

        Returns:
            pandas dataframe

        """
        raise NotImplementedError
