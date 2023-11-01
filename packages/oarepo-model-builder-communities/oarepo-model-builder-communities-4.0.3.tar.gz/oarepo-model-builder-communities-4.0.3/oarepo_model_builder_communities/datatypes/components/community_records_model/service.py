from oarepo_model_builder.datatypes.components import ServiceModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from ... import CommunityRecordsDataType


class CommunityRecordsServiceModelComponent(ServiceModelComponent):
    eligible_datatypes = [CommunityRecordsDataType]
    dependency_remap = ServiceModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        config = set_default(datatype, "service-config", {})
        config.setdefault(
            "base-classes",
            ["oarepo_communities.services.community_records.config.CommunityRecordsServiceConfig"],
        )
        config.setdefault("imports", [])

        service = set_default(datatype, "service", {})
        service.setdefault("base-classes", ["oarepo_communities.services.community_records.service.CommunityRecordsService"])
        service.setdefault("imports", [])

        service.setdefault("proxy", "current_community_records_service")
        service.setdefault(
            "additional-args",
            ["record_communities_service=self.service_record_communities"],
        )
        super().before_model_prepare(datatype, context=context, **kwargs)

    def after_model_prepare(self, datatype, *, context, **kwargs):
        datatype.definition["service-config"]["components"] = []
