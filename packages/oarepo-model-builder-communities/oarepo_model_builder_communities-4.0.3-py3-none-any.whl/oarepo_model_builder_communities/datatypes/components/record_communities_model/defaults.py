from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.datatypes.components import DefaultsModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from ....datatypes import RecordCommunitiesDataType


class RecordCommunitiesDefaultsModelComponent(DefaultsModelComponent):
    eligible_datatypes = [RecordCommunitiesDataType]
    dependency_remap = DefaultsModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        published_record_datatype: DataType = context["published_record"]
        # parent_file_record_prefix = parent_record_datatype.definition["module"]["prefix"]
        # parent_file_record_alias = parent_record_datatype.definition["module"]["alias"]

        module = set_default(datatype, "module", {})
        module.setdefault(
            "qualified", published_record_datatype.definition["module"]["qualified"]
        )
        module.setdefault(
            "prefix",
            f"{published_record_datatype.definition['module']['prefix']}RecordCommunities",
        )
        # module.setdefault("prefix", f"{parent_file_record_prefix}Draft")
        # module.setdefault("alias", f"{parent_file_record_alias}_draft")

        super().before_model_prepare(datatype, context=context, **kwargs)
