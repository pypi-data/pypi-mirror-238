from amsdal_utils.classes.version_manager import ClassVersionManager
from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.models.data_models.reference import Reference
from amsdal_utils.models.data_models.reference import ReferenceData
from amsdal_utils.models.enums import Versions


def build_reference(
    class_name: str,
    object_id: str,
    class_version: str | Versions = Versions.LATEST,
    object_version: str | Versions = Versions.LATEST,
    resource: str | None = None,
) -> Reference:
    connection_name = resource or AmsdalConfigManager().get_connection_name_by_model_name(class_name)

    if class_version == Versions.LATEST:
        class_version = ClassVersionManager().get_latest_class_version(class_name).version

        if not class_version:
            class_version = Versions.LATEST

    return Reference(
        ref=ReferenceData(
            resource=connection_name,
            class_name=class_name,
            class_version=class_version,
            object_id=object_id,
            object_version=object_version,
        ),
    )
