from pathlib import Path
from typing import List, Union

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.profiles.record import RecordProfile
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.utils.dict import dict_get


class RecordCommunitiesProfile(RecordProfile):
    default_model_path = ["record", "record-communities"]

    @classmethod
    def get_default_profile_context(
        cls, model: ModelSchema, model_path=None, profile=None
    ):
        if model_path is None:
            model_path = RecordCommunitiesProfile.default_model_path
        if profile is None:
            profile = "record_communities"
        return {
            "profile": profile,
            "model_path": model_path,
            "context": {
                "published_record": model.get_schema_section("record", model_path[:-1]),
                "profile": "record_communities",
                "profile_module": "record_communities",
                "switch_profile": True,
            },
        }

    def build(
        self,
        model: ModelSchema,
        profile: str,
        model_path: List[str],
        output_directory: Union[str, Path],
        builder: ModelBuilder,
        **kwargs,
    ):
        ctx = RecordCommunitiesProfile.get_default_profile_context(
            model, model_path, profile
        )
        # file_record = model.get_schema_section("files", model_path[:-1] + ["files"])

        record_communities_profile = dict_get(model.schema, model_path)
        record_communities_profile.setdefault("type", "record_communities")

        # pass the parent record as an extra context item. This will be handled by file-aware
        # components in their "prepare" method
        super().build(
            model=model,
            profile=ctx["profile"],
            model_path=ctx["model_path"],
            output_directory=output_directory,
            builder=builder,
            context=ctx["context"],
        )
