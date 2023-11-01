from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class RecordCommunitiesServiceConfigAdditionalBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "record_communities_service_config_add"
    section = "service-config"
    template = "service-config-additional"

    def finish(self, **extra_kwargs):
        super().finish(
            published_record=self.current_model.published_record, **extra_kwargs
        )
