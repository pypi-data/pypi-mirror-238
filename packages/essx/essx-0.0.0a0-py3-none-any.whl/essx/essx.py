# Copyright 2023 StreamSets Inc.

import enum
import os
import uuid
import pymysql
import pandas as pd
import snowflake.connector
import logging

from typing import OrderedDict, List, Any, Dict, Literal

from streamsets.sdk.sch import ControlHub
from streamsets.sdk.sch_models import Pipeline, Engine, SchStStage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ASTER_URL = 'https://dev.login.streamsets.com'


class JoinType(enum.Enum):
    CROSS = 'cross'
    INNER = 'inner'
    LEFT = 'left'
    RIGHT = 'right'


class TargetType(enum.Enum):
    INTEGER = int
    STRING = str
    # Add more targets as needed


class SortType(enum.Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class StageType(enum.Enum):
    ORIGIN = 'origin'
    PROCESSOR = 'processor'
    DESTINATION = 'destination'


class DataFrameOperation(enum.Enum):
    ASTYPE = 'astype'
    DROP = 'drop'
    SORT_VALUES = 'sort_values'
    REPLACE = 'replace'
    GROUPBY = 'groupby'
    AGG = 'agg'
    LOC = 'loc'
    SX = 'sx'
    # Add more operations as needed


class MySQLConnection:
    def __init__(self, host: str, username: str, database: str):
        self.host = host
        self.username = username
        self.database = database
        self._password = os.getenv('MYSQL_P')

    @property
    def password(self):
        return self._password

    def validate(self):
        try:
            connection = pymysql.Connect(
                host=self.host, user=self.username, password=self._password, database=self.database
            )
            connection.close()
        except pymysql.Connect.Error as err:
            logger.error(f"MySQL connection validation failed: {err}")
            return False

        logger.info("MySQL connection validated successfully")
        return True


class SnowflakeConnection:
    def __init__(self, account, role, database, schema, username, warehouse):
        self.account = account
        self.role = role
        self.database = database
        self.schema = schema
        self.username = username
        self._warehouse = warehouse
        self._password = os.getenv('SF_P')

    @property
    def password(self):
        return self._password

    @property
    def warehouse(self):
        return self._warehouse

    def connect(self):
        try:
            connection = snowflake.connector.connect(
                user=self.username,
                password=self._password,
                account=self.account,
                warehouse=self._warehouse,
                database=self.database,
                schema=self.schema
            )
            connection.close()
        except snowflake.connector.errors.DatabaseError as err:
            logger.error(f"Snowflake connection failed: {err}")
            return False

        logger.info("Snowflake connection successful")
        return True


class SxDataFrame:
    def __init__(self, stage_type: StageType, cfg: List[dict] | None, df: pd.DataFrame):
        self.id = uuid.uuid4().hex[:5]
        self.type = stage_type
        self.cfg = cfg
        self._df = df
        self._next = []

    def __repr__(self):
        return repr(self._df)

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._df, attr)

    def __getitem__(self, item):
        return self._df[item]

    def __setitem__(self, item, data):
        self._df[item] = data

    def process_dataframe_operation(self,
                                    operation_name: DataFrameOperation,
                                    stage_config: List[Dict],
                                    stage_type: StageType,
                                    **kwargs: Any) -> 'SxDataFrame':
        """
        Process a DataFrame operation (astype, drop, sort_values, replace),
        create a new SxDataFrame, and add a graph node for tracking.

        Parameters:
        - operation_name: Name of the DataFrame operation (e.g., 'astype', 'drop').
        - stage_config: Configuration for additional stages.
        - kwargs: Keyword arguments for the operation.

        Returns:
        A new SxDataFrame resulting from the specified DataFrame operation.
        """

        logger.info(f"Processing DataFrame operation: {operation_name}")

        # Perform the specified DataFrame operation on the underlying Pandas DataFrame
        df = getattr(self._df, operation_name.value)(**kwargs)

        # Create a new SxDataFrame with the result of the DataFrame operation
        node = SxDataFrame(stage_type, stage_config, df)
        self._next.append(node)

        logger.info(f"DataFrame operation '{operation_name}' completed")

        return node

    @property
    def df(self):
        return self._df

    @property
    def next(self):
        return self._next

    def drop(self, **kwargs: Any) -> 'SxDataFrame':

        field_remover = dict(name='Field Remover',
                             action='REMOVE',
                             match_criteria='NAMED',
                             fields=kwargs.get('columns'))
        stage_configs = [field_remover]

        return self.process_dataframe_operation(DataFrameOperation.DROP, stage_configs, StageType.PROCESSOR, **kwargs)

    def replace(self, **kwargs: Any) -> 'SxDataFrame':

        stream_selector = dict(name='Stream Selector',
                               condition=[f'{kwargs.get("columns")} == "{kwargs.get("old")}"', "default"])
        field_replacer = dict(name='Field Replacer',
                              replacement_rules=[{'setToNull': False,
                                                  'fields': f'{kwargs.get("columns")}',
                                                  'replacement': f"{kwargs.get('new')}"}])
        stage_configs = [stream_selector, field_replacer]

        return self.process_dataframe_operation(DataFrameOperation.REPLACE, stage_configs, StageType.PROCESSOR, **kwargs)

    def astype(self, **kwargs: Any) -> 'SxDataFrame':

        try:
            target_type = next(member for member in TargetType if member.value == kwargs.get('value_type'))
        except StopIteration:
            raise ValueError(f"Invalid value_type. Expected one of: {', '.join(e.name for e in TargetType)}")

        type_converter = dict(name='Type Converter',
                              conversions=[dict(fieldName=kwargs.get("columns"),
                                                targetType=target_type.name)])
        stage_configs = [type_converter]

        return self.process_dataframe_operation(DataFrameOperation.ASTYPE, stage_configs, StageType.PROCESSOR, **kwargs)

    def sort_values(self, **kwargs: Any) -> 'SxDataFrame':

        order = SortType.ASC.value if kwargs.get('ascending') else SortType.DESC.value

        sort = dict(name='Sort', configs=[{'col': kwargs.get('by'), 'order': order}])
        stage_configs = [sort]

        return self.process_dataframe_operation(DataFrameOperation.SORT_VALUES, stage_configs, StageType.PROCESSOR, **kwargs)

    def groupby(self):
        # Aggregate
        pass

    def agg(self):
        # Aggregate
        pass

    def loc(self):
        # Filter
        pass

    def to_jdbc(self):
        pass

    def to_s3(self):
        pass

    def to_snowflake(self, connection: SnowflakeConnection, table):

        if not self._pipeline:
            raise ValueError('No pipeline is configured in this context. '
                             'Please define a SX object to use a new data source.')

        snowflake_stage = dict(name='Snowflake')
        configuration = dict(use_credentials=True,
                             account=connection.account,
                             user=connection.username,
                             password=connection.password,
                             include_organization=False,
                             use_snowflake_role=True,
                             snowflake_role_name=connection.role,
                             warehouse='SDK_TESTING',
                             database=connection.database,
                             schema=connection.schema,
                             read_mode='TABLE',
                             table=table)
        snowflake_stage.update(configuration)

        stage_configs = [snowflake_stage]

        return self.process_dataframe_operation(DataFrameOperation.SX, stage_configs, StageType.DESTINATION)


class Sx:
    def __init__(self):
        self.id = uuid.uuid4()
        self.name = f'ESSX_{uuid.uuid4()}'
        self._sch = ControlHub(credential_id=os.getenv('SCH_CREDENTIAL_ID'),
                               token=os.getenv('SCH_TOKEN'),
                               aster_url=os.getenv('ASTER_URL'))
        self._engine = self._get_authoring_engine()
        self._pipeline = self._create_pipeline()
        self.sources = []
        self.destinations = []
        self._df_to_stage = {}

    def _create_pipeline(self) -> Pipeline:
        pipeline_builder = self._sch.get_pipeline_builder(engine_type='transformer', engine_id=self._engine.id)
        pipeline = pipeline_builder.build(self.name)
        self._sch.publish_pipeline(pipeline, draft=True)

        return pipeline

    def _create_stage(self, config: dict, stage_type: StageType) -> SchStStage:

        stage = self._pipeline.add_stage(config.get('name'), type=stage_type.value)

        # Update attributes based on the dictionary configuration
        for key, value in config.items():
            if key == 'name':
                continue

            if key == 'configuration':
                setattr(stage.configuration, key, value)
            else:
                setattr(stage, key, value)

        return stage

    def _create_source(self, origin_name: str,
                       configuration: Dict,
                       preview_size: int = 10,
                       remote: bool = False) -> SxDataFrame:
        if not self._pipeline:
            raise ValueError('No pipeline is configured in this context. '
                             'Please define a SX object to use a new data source.')

        origin_config = dict(name=origin_name)
        origin_config.update(configuration)

        stage = self._create_stage(origin_config, StageType.ORIGIN)
        self._sch.publish_pipeline(self._pipeline, draft=True)

        preview_data = self._get_preview_data(batch_size=preview_size,
                                              stage_instance_name=stage.instance_name,
                                              remote=remote)

        pd_df = self._create_data_frame(preview_data)
        df = SxDataFrame(StageType.ORIGIN, None, pd_df)
        self.sources.append(df)
        self._df_to_stage[df.id] = stage

        return df

    @staticmethod
    def _create_data_frame(preview_data) -> pd.DataFrame:
        records = {}
        for item in preview_data:
            for key, field in item.items():
                if key in records:
                    records[key].append(field.value)
                else:
                    records[key] = [field.value]

        return pd.DataFrame.from_dict(records)

    def _get_authoring_engine(self) -> Engine:
        engine = self._sch.engines.get(engine_type='TRANSFORMER', responding=True)
        return engine

    def _get_preview_data(self,
                          batch_size: int,
                          stage_instance_name: str,
                          remote: bool = False) -> List[OrderedDict]:

        executor_instance, executor_pipeline_id = self._sch._add_pipeline_to_executor_if_not_exists(self._pipeline)
        preview = executor_instance.run_pipeline_preview(pipeline_id=executor_pipeline_id,
                                                         batches=1,
                                                         batch_size=batch_size,
                                                         skip_targets=True,
                                                         end_stage=None,
                                                         timeout=120000,
                                                         test_origin=False,
                                                         wait=True,
                                                         remote=remote)

        batches = preview.preview.preview_batches
        preview_field = [item.field for item in batches[0].stage_outputs[stage_instance_name].output]

        return preview_field

    def from_jdbc(self):
        pass

    def from_s3(self):
        pass

    def from_csv(self, path: str, preview_size: int = 10, remote: bool = False) -> SxDataFrame:
        directory_path = os.path.dirname(path)
        file_name = os.path.basename(path)

        configuration = dict(use_credentials=True,
                             directory_path=directory_path,
                             file_name_pattern=file_name,
                             data_format='CSV')

        return self._create_source('File', configuration, preview_size, remote)

    def from_mysql(self, connection: MySQLConnection,
                   schema: str,
                   tables: List[str],
                   preview_size=10,
                   remote: bool = False) -> SxDataFrame:

        configuration = dict(use_credentials=True,
                             username=connection.username,
                             password=connection.password,
                             jdbc_connection_string=f'jdbc:mysql://{connection.host}',
                             schema=schema,
                             tables=tables)

        return self._create_source('MySQL JDBC Table', configuration, preview_size, remote)

    def from_snowflake(self, connection: SnowflakeConnection, table, preview_size=10, remote: bool = False):
        configuration = dict(use_credentials=True,
                             account=connection.account,
                             user=connection.username,
                             password=connection.password,
                             include_organization=False,
                             use_snowflake_role=True,
                             snowflake_role_name=connection.role,
                             warehouse='SDK_TESTING',
                             database=connection.database,
                             schema=connection.schema,
                             read_mode='TABLE',
                             table=table)

        return self._create_source('Snowflake', configuration, preview_size, remote)

    def merge(self,
              left: SxDataFrame,
              right: SxDataFrame,
              how: Literal["left", "right", "inner", "outer", "cross"] = 'inner',
              on: list = None):

        if not self._pipeline:
            raise ValueError('No pipeline is configured in this context. '
                             'Please define a SX object to use a new data source.')

        join_stage = dict(name='Join', inputs=[left, right])
        configuration = dict(join_type=how.upper(),
                             matching_fields=[on] if not isinstance(on, list) else on)
        join_stage.update(configuration)

        stage_configs = [join_stage]
        pd_df = pd.merge(left.df, right.df, on=on, how=how)
        df = SxDataFrame(StageType.PROCESSOR, stage_configs, pd_df)

        left.next.append(df)
        right.next.append(df)

        return df

    def traverse(self, commit: bool = False):
        result = []
        visited = set()
        current_level = self.sources

        while current_level:
            level_data = []
            next_level = []

            for node in current_level:
                if node.id in visited:
                    continue

                level_data.append(node)
                visited.add(node.id)
                next_level.extend(node.next)

                if commit:

                    # TODO: SxDataFrame operations may span multiple stages for pandas replication

                    prev = self._df_to_stage[node.id]
                    for sx_df in node.next:
                        stage = self._df_to_stage.get(sx_df.id)
                        if not stage:
                            stage = self._create_stage(sx_df.cfg[0], sx_df.type)
                            self._df_to_stage[sx_df.id] = stage
                        stage.connect_inputs([prev])

            if level_data:
                result.append(level_data)

            current_level = next_level

        return result

    def commit(self) -> None:
        if not self._pipeline.draft:
            return None

        self.traverse(commit=True)
        self._sch.publish_pipeline(self._pipeline, draft=True)

        job_builder = self._sch.get_job_builder()
        job = job_builder.build(job_name=f'{self.name}_job', pipeline=self._pipeline)
        self._sch.add_job(job)

    def reset(self) -> None:
        self._sch.delete_pipeline(self._pipeline)
        self._pipeline = None
