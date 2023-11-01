from pathlib import Path
from typing import List, Union

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.profiles.record import RecordProfile
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.utils.dict import dict_get


class CommunityRecordsProfile(RecordProfile):
    default_model_path = ["record", "community-records"]

    def build(
        self,
        model: ModelSchema,
        profile: str,
        model_path: List[str],
        output_directory: Union[str, Path],
        builder: ModelBuilder,
        **kwargs,
    ):
        published_record = model.get_schema_section("record", model_path[:-1])
        # file_record = model.get_schema_section("files", model_path[:-1] + ["files"])

        community_records_profile = dict_get(model.schema, model_path)
        community_records_profile.setdefault("type", "community_records")

        # pass the parent record as an extra context item. This will be handled by file-aware
        # components in their "prepare" method
        super().build(
            model=model,
            profile=profile,
            model_path=model_path,
            output_directory=output_directory,
            builder=builder,
            context={
                "published_record": published_record,
                "profile": "community_records",
                "profile_module": "community_records",
                "switch_profile": True,
            },
        )
