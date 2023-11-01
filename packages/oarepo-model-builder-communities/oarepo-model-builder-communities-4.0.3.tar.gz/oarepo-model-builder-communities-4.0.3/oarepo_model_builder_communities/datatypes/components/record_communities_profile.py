import marshmallow as ma
from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType, Section
from oarepo_model_builder.datatypes.components import DefaultsModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder.utils.python_name import base_name

from oarepo_model_builder_communities.profiles.record_communities import (
    RecordCommunitiesProfile,
)


def get_record_communities_schema():
    from ..communities import RecordCommunitiesDataType

    return RecordCommunitiesDataType.validator()


class RecordCommunitiesComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    affects = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        record_communities = ma.fields.Nested(
            get_record_communities_schema,
            data_key="record-communities",
            attribute="record-communities",
        )

    def process_links(self, datatype, section: Section, **kwargs):
        if datatype.root.profile == "record_communities":
            section.config = {}

    def process_mb_invenio_drafts_parent_extra_fields(
        self, datatype, section: Section, **kwargs
    ):
        if (
            hasattr(datatype, "published_record")
            and "record-communities" in datatype.published_record.definition
        ):
            ctx = RecordCommunitiesProfile.get_default_profile_context(datatype.schema)
            record_communities_record = datatype.schema.get_schema_section(
                ctx["profile"], ctx["model_path"], prepare_context=ctx["context"]
            )
            """
            record_communities_record = datatype.schema.get_schema_section(
                "record_communities",
                ["record", "record-communities"],
                prepare_context={
                    "profile": "record_communities",
                    "published_record": datatype.schema.get_schema_section(
                        "record", ["record"]
                    ),
                    "profile_module": "record_communities",
                },
            )
            """
            additional_parent_fields = {}
            additional_parent_fields["additional-fields"] = [
                f"communities = CommunitiesField({base_name(record_communities_record.definition['record-metadata']['class'])})"
            ]

            additional_parent_fields["imports"] = [
                {
                    "import": "invenio_communities.records.records.systemfields.CommunitiesField"
                },
                {
                    "import": record_communities_record.definition["record-metadata"][
                        "class"
                    ],
                },
            ]
            section.config["additional-parent-fields"] = additional_parent_fields

    def process_mb_invenio_drafts_record_communities_service_config(
        self, datatype, section: Section, **kwargs
    ):
        if (
            hasattr(datatype, "published_record")
            and "record-communities" in datatype.published_record.definition
        ):
            ctx = RecordCommunitiesProfile.get_default_profile_context(datatype.schema)
            record_communities_record = datatype.schema.get_schema_section(
                ctx["profile"], ctx["model_path"], prepare_context=ctx["context"]
            )

            """
            record_communities_record = datatype.schema.get_schema_section(
                "record_communities",
                ["record", "record-communities"],
                prepare_context={
                    "profile": "record_communities",
                    "published_record": datatype.schema.get_schema_section(
                        "record", ["record"]
                    ),
                    "profile_module": "record_communities",
                },
            )
            """
            section.config[
                "record-communities-service-config"
            ] = record_communities_record.definition["service-config"]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile == "record_communities":
            set_default(datatype, "search-options", {}).setdefault("skip", True)
            set_default(datatype, "permissions", {}).setdefault("skip", True)
