from oarepo_model_builder.datatypes.components import BlueprintsModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from ... import CommunityRecordsDataType


class CommunityRecordsBlueprintsModelComponent(BlueprintsModelComponent):
    eligible_datatypes = [CommunityRecordsDataType]
    dependency_remap = BlueprintsModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        published_record = context["published_record"]
        api = set_default(datatype, "api-blueprint", {})
        api.setdefault(
            "alias",
            f"{published_record.definition['api-blueprint']['alias']}_community_record",
        )
        app = set_default(datatype, "app-blueprint", {})
        app.setdefault(
            "alias",
            f"{published_record.definition['app-blueprint']['alias']}_community_record",
        )

        super().before_model_prepare(datatype, context=context, **kwargs)
