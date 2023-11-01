from oarepo_model_builder.datatypes.components import ResourceModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from ... import CommunityRecordsDataType


class CommunityRecordsResourceModelComponent(ResourceModelComponent):
    eligible_datatypes = [CommunityRecordsDataType]
    dependency_remap = ResourceModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        config = set_default(datatype, "resource-config", {})
        config.setdefault("base-classes", ["oarepo_communities.resources.community_records.config.CommunityRecordsResourceConfig"])
        config.setdefault("imports", [])
        config.setdefault("base-url", "/communities/")
        resource = set_default(datatype, "resource", {})
        resource.setdefault("base-classes", ["oarepo_communities.resources.community_records.resource.CommunityRecordsResource"])
        resource.setdefault("imports", [])
        resource.setdefault("proxy", "current_community_records_resource")
        super().before_model_prepare(datatype, context=context, **kwargs)
