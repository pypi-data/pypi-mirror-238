
from oarepo_model_builder.datatypes.components.model.record_metadata import (
    RecordMetadataModelComponent,
)
from oarepo_model_builder.datatypes.components.model.utils import set_default

from ... import CommunityRecordsDataType, RecordCommunitiesDataType


class CommunityRecordMetadataModelComponent(RecordMetadataModelComponent):
    eligible_datatypes = [CommunityRecordsDataType, RecordCommunitiesDataType]
    dependency_remap = RecordMetadataModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        metadata = set_default(datatype, "record-metadata", {})
        metadata.setdefault(
            "base-classes",
            ["invenio_db.db{db.Model}", "invenio_communities.records.records.models.CommunityRelationMixin"],
        )
        metadata.setdefault("imports", [])

        metadata.setdefault(
            "module",
            context["published_record"].definition["record-metadata"]["module"],
        )
        # pdb.set_trace()
        metadata.setdefault("use-versioning", False)
        super().before_model_prepare(datatype, context=context, **kwargs)
