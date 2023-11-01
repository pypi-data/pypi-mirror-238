from spprval.database.DataSource import DataSource
from spprval.database.Adapter import DBAdapter


class DBWrapper(DataSource):
    def __init__(self, connector=None, level=None):
        # Default value for connector if not provided
        if connector is None:
            connector = DBAdapter
        # Default value for level if not provided
        if level is None:
            level = connector.GRANULARY

        self.adapter = connector
        self.level = level

    def get_data(self, pools, res_names):
        validation_dataset_list = []
        for df in self.adapter.get_works_by_pulls(
            work_pulls=pools,
            resource_list=res_names,
            key=self.level,
            res_key=self.adapter.GRANULARY,
        ):
            if df is not None:
                df.fillna(0, inplace=True)
            validation_dataset_list.append(df)
        return validation_dataset_list

    def get_act_names(self):
        df = self.adapter.get_all_works_name()
        return df

    def get_res_names(self):
        df = self.adapter.get_all_resources_name()
        return df
