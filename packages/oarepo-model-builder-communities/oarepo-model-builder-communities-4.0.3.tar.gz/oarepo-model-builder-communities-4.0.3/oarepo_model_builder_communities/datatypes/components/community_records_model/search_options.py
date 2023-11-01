from oarepo_model_builder.datatypes.components import SearchOptionsModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from ... import CommunityRecordsDataType


class CommunityRecordsSearchOptionsModelComponent(SearchOptionsModelComponent):
    eligible_datatypes = [CommunityRecordsDataType]
    dependency_remap = SearchOptionsModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        published_record = context["published_record"].definition

        record_search_options = set_default(datatype, "search-options", {})
        record_search_options.setdefault(
            "module", published_record["search-options"]["module"]
        )
        record_search_options.setdefault(
            "class", published_record["search-options"]["class"]
        )
        super().before_model_prepare(datatype, context=context, **kwargs)
