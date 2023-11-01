from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class CommunityRecordsTestResourcesBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "community_records_test_resources"
    template = "community-records-test-resources"

    def _get_output_module(self):
        return f'{self.current_model.definition["tests"]["module"]}.communities.test_community_records_resources'

    def finish(self, **extra_kwargs):
        tests = getattr(self.current_model, "section_tests")
        super().finish(
            fixtures=tests.fixtures,
            test_constants=tests.constants,
            published_record=self.current_model.published_record,
            **extra_kwargs,
        )
