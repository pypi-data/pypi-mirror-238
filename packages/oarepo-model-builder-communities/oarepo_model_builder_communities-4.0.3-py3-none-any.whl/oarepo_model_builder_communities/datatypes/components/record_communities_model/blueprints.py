from oarepo_model_builder.datatypes.components import BlueprintsModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from ....datatypes import RecordCommunitiesDataType


class RecordCommunitiesBlueprintsModelComponent(BlueprintsModelComponent):
    eligible_datatypes = [RecordCommunitiesDataType]
    dependency_remap = BlueprintsModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        published_record = context["published_record"]
        api = set_default(datatype, "api-blueprint", {})
        api.setdefault(
            "alias",
            f"{published_record.definition['api-blueprint']['alias']}_record_communities",
        )
        app = set_default(datatype, "app-blueprint", {})
        app.setdefault(
            "alias",
            f"{published_record.definition['app-blueprint']['alias']}_record_communities",
        )

        super().before_model_prepare(datatype, context=context, **kwargs)
