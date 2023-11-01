from oarepo_model_builder.datatypes.components import ServiceModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from ...communities import RecordCommunitiesDataType


class RecordCommunitiesServiceModelComponent(ServiceModelComponent):
    eligible_datatypes = [RecordCommunitiesDataType]
    dependency_remap = ServiceModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        config = set_default(datatype, "service-config", {})
        config.setdefault(
            "base-classes",
            ["oarepo_communities.services.record_communities.config.RecordCommunitiesServiceConfig"],
        )
        config.setdefault("imports", [])

        service = set_default(datatype, "service", {})
        service.setdefault("base-classes", ["oarepo_communities.services.record_communities.service.RecordCommunitiesService"])
        service.setdefault("imports", [])
        service.setdefault(
            "additional-args",
            ["record_service=self.service_records"],
        )
        service.setdefault("proxy", "current_record_communities_service")
        super().before_model_prepare(datatype, context=context, **kwargs)

    def after_model_prepare(self, datatype, *, context, **kwargs):
        datatype.definition["service-config"]["components"] = []
