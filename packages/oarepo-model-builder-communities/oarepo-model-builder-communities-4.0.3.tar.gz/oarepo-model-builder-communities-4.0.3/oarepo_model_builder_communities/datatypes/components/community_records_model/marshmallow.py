# oarepo_communities.schemas.record_communities.RecordCommunitiesSchema

from oarepo_model_builder.datatypes.components import MarshmallowModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from ... import CommunityRecordsDataType


class CommunityRecordsMarshmallowModelComponent(MarshmallowModelComponent):
    eligible_datatypes = [CommunityRecordsDataType]
    dependency_remap = MarshmallowModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        ma = set_default(datatype, "marshmallow", {})
        ma.setdefault(
            "class", context["published_record"].definition["marshmallow"]["class"]
        )
        super().before_model_prepare(datatype, context=context, **kwargs)
