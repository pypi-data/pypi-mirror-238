from amsdal_models.classes.model import Model
from starlette.authentication import BaseUser

from amsdal_server.apps.classes.errors import ClassNotFoundError
from amsdal_server.apps.classes.mixins.column_info_mixin import ColumnInfoMixin
from amsdal_server.apps.classes.mixins.model_class_info import ModelClassMixin
from amsdal_server.apps.classes.serializers.class_info import ClassInfo
from amsdal_server.apps.common.mixins.permissions_mixin import PermissionsMixin
from amsdal_server.apps.objects.mixins.object_data_mixin import ObjectDataMixin


class ClassesApi(PermissionsMixin, ModelClassMixin, ColumnInfoMixin, ObjectDataMixin):
    @classmethod
    def get_classes(cls, user: BaseUser) -> list[ClassInfo]:
        classes: list[Model] = cls.get_class_objects_qs().execute()
        result: list[ClassInfo] = []

        for class_item in classes:
            result.append(cls.get_class(user, class_item))

        return result

    @classmethod
    def get_class_by_name(
        cls,
        user: BaseUser,
        class_name: str,
    ) -> ClassInfo:
        class_item: Model | None = cls.get_class_objects_qs().filter(title=class_name).first().execute()

        if not class_item:
            msg = f'Class not found: {class_name}'
            raise ClassNotFoundError(class_name, msg)

        return cls.get_class(user, class_item)

    @classmethod
    def get_class(
        cls,
        user: BaseUser,
        class_item: Model,
    ) -> ClassInfo:
        model_class = cls.get_model_class(class_item)
        permissions_info = cls.get_permissions_info(model_class, user)
        class_properties = cls.get_class_properties_by_class_name(class_item.title)  # type: ignore[attr-defined]
        class_info = ClassInfo(
            **{
                'class': class_item.title,  # type: ignore[attr-defined]
                'count': 0,
                'properties': class_properties,
            },
        )

        if permissions_info.has_read_permission:
            class_info.count = (
                model_class.objects.filter(
                    _metadata__is_deleted=False,
                )
                .count()
                .execute()
            )

        return class_info
