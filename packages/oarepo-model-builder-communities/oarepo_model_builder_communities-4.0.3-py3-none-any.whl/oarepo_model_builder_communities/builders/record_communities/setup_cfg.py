from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.outputs.cfg import CFGOutput


class RecordCommunitiesSetupCfgBuilder(OutputBuilder):
    TYPE = "record_communities_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        output.add_dependency("oarepo-communities", ">=4.0.3")
