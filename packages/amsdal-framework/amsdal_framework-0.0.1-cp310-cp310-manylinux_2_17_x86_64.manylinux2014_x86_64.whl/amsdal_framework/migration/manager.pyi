from _typeshed import Incomplete
from amsdal_data.table_schemas.manager import TableSchemasManager
from amsdal_framework.schemas.manager import SchemaManager as SchemaManager
from amsdal_models.classes.manager import ClassManager
from amsdal_models.classes.model import Model
from amsdal_models.schemas.data_models.schema import ObjectSchema
from amsdal_utils.models.data_models.table_schema import TableSchema as TableSchema
from amsdal_utils.models.enums import SchemaTypes

class MigrationManager:
    _schema_manager: Incomplete
    _table_schemas_manager: Incomplete
    _class_manager: Incomplete
    def __init__(self, schema_manager: SchemaManager, table_schema_manager: TableSchemasManager, class_manager: ClassManager) -> None: ...
    def run_migrations(self) -> None: ...
    def _migrate_class(self, object_schema: ObjectSchema, base_class: type[Model], schema_type: SchemaTypes) -> tuple[Model, bool]: ...
    def _register_class_version(self, schema: TableSchema, *, create_table: bool = ...) -> None: ...
    def _migrate_class_objects(self, class_name: str, prior_version: str, new_version: str, schema_type: SchemaTypes) -> None: ...
