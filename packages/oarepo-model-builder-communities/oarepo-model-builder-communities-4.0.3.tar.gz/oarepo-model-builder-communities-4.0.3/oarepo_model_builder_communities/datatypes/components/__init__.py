from .community_records_model import (
    CommunityRecordsBlueprintsModelComponent,
    CommunityRecordsDefaultsModelComponent,
    CommunityRecordsExtResourceModelComponent,
    CommunityRecordsMarshmallowModelComponent,
    CommunityRecordsResourceModelComponent,
    CommunityRecordsSearchOptionsModelComponent,
    CommunityRecordsServiceModelComponent,
)
from .community_records_profile import CommunityRecordsComponent
from .record_communities_model import (
    RecordCommunitiesBlueprintsModelComponent,
    RecordCommunitiesDefaultsModelComponent,
    RecordCommunitiesExtResourceModelComponent,
    RecordCommunitiesMarshmallowModelComponent,
    RecordCommunitiesResourceModelComponent,
    RecordCommunitiesServiceModelComponent,
)
from .record_communities_profile import RecordCommunitiesComponent
from .shared import CommunityRecordMetadataModelComponent, CommunityRecordModelComponent

RECORD_COMMUNITIES_COMPONENTS = [
    RecordCommunitiesResourceModelComponent,
    RecordCommunitiesServiceModelComponent,
    RecordCommunitiesComponent,
    RecordCommunitiesExtResourceModelComponent,
    RecordCommunitiesDefaultsModelComponent,
    RecordCommunitiesMarshmallowModelComponent,
    RecordCommunitiesBlueprintsModelComponent,
]

COMMUNITY_RECORDS_COMPONENTS = [
    CommunityRecordsResourceModelComponent,
    CommunityRecordsServiceModelComponent,
    CommunityRecordsComponent,
    CommunityRecordsExtResourceModelComponent,
    CommunityRecordsDefaultsModelComponent,
    CommunityRecordsMarshmallowModelComponent,
    CommunityRecordsBlueprintsModelComponent,
    CommunityRecordsSearchOptionsModelComponent,
]
# todo rename
SHARED_COMPONENTS = [
    CommunityRecordMetadataModelComponent,
    CommunityRecordModelComponent,
]
