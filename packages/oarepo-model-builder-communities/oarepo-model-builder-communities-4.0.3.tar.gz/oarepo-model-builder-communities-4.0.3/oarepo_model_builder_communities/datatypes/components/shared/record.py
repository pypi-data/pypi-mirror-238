from oarepo_model_builder.datatypes.components import RecordModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from ... import CommunityRecordsDataType, RecordCommunitiesDataType


class CommunityRecordModelComponent(RecordModelComponent):
    eligible_datatypes = [CommunityRecordsDataType, RecordCommunitiesDataType]
    dependency_remap = RecordModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        record = set_default(datatype, "record", {})
        record.setdefault(
            "class", f"{context['published_record'].definition['record']['class']}"
        )
        super().before_model_prepare(datatype, context=context, **kwargs)
