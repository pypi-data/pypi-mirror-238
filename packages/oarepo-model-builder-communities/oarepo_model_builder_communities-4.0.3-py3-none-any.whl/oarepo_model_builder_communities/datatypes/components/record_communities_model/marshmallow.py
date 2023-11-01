# oarepo_communities.schemas.record_communities.RecordCommunitiesSchema

from oarepo_model_builder.datatypes.components import MarshmallowModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from oarepo_model_builder_communities.datatypes import RecordCommunitiesDataType


class RecordCommunitiesMarshmallowModelComponent(MarshmallowModelComponent):
    eligible_datatypes = [RecordCommunitiesDataType]
    dependency_remap = MarshmallowModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        ma = set_default(datatype, "marshmallow", {})
        ma.setdefault(
            "class",
            "oarepo_communities.services.record_communities.schema.RecordCommunitiesSchema",
        )
        super().before_model_prepare(datatype, context=context, **kwargs)
