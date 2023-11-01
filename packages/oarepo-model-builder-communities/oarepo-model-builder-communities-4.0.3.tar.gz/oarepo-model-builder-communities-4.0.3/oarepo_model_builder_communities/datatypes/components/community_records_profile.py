import marshmallow as ma
from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType, Section
from oarepo_model_builder.datatypes.components import DefaultsModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default


def get_community_records_schema():
    from ..communities import CommunityRecordsDataType

    return CommunityRecordsDataType.validator()


class CommunityRecordsComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    affects = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        community_records = ma.fields.Nested(
            get_community_records_schema,
            data_key="community-records",
            attribute="community-records",
        )

    def process_links(self, datatype, section: Section, **kwargs):
        if datatype.root.profile == "community_records":
            section.config = {}

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile == "community_records":
            set_default(datatype, "permissions", {}).setdefault("skip", True)
