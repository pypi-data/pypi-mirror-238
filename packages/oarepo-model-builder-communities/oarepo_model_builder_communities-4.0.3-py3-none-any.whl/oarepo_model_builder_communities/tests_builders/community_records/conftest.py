from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class CommunityRecordsConftestBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "community_records_conftest"
    template = "community-records-conftest"

    def _get_output_module(self):
        return f'{self.current_model.definition["tests"]["module"]}.conftest'
