import marshmallow as ma
from oarepo_model_builder.datatypes import DataTypeComponent
from oarepo_model_builder.datatypes.components import DefaultsModelComponent
from oarepo_model_builder.datatypes.components.model.ext_resource import (
    ExtResourceSchema,
)
from oarepo_model_builder.datatypes.components.model.utils import set_default

from oarepo_model_builder_communities.datatypes import RecordCommunitiesDataType


class RecordCommunitiesExtResourceModelComponent(DataTypeComponent):
    eligible_datatypes = [RecordCommunitiesDataType]
    depends_on = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        ext_resource = ma.fields.Nested(
            ExtResourceSchema,
            attribute="ext-resource",
            data_key="ext-resource",
        )

    def process_ext_resource(self, datatype, section, **kwargs):
        if datatype.root.profile == "record_communities":
            cfg = section.config
            cfg["ext-service-name"] = "service_record_communities"
            cfg["ext-resource-name"] = "resource_record_communities"

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if not datatype.root.profile == "record_communities":
            return
        ext = set_default(datatype, "ext-resource", {})

        ext.setdefault("generate", True)
        ext.setdefault("skip", False)
