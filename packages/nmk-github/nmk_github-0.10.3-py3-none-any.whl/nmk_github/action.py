from typing import Dict, List

from nmk.model.resolver import NmkListConfigResolver
from nmk.utils import is_condition_set
from nmk_base.common import TemplateBuilder

# Conditional steps keys
KEY_IF = "__if__"
KEY_UNLESS = "__unless__"
KEY_NAME = "name"


class ActionFileBuilder(TemplateBuilder):
    def filter_steps(self, steps: List[Dict[str, str]]) -> List[Dict[str, str]]:
        # Browse steps
        out = []
        for step in steps:
            added_step = dict(step)

            # Check conditions
            ok_to_add = True
            for key, expected in [(KEY_IF, True), (KEY_UNLESS, False)]:
                if key in added_step:
                    if is_condition_set(added_step[key]) != expected:
                        self.logger.debug(f"'{key}' condition not met for build step '{added_step[KEY_NAME]}': {added_step[key]}")  # NOQA: B028
                        ok_to_add = False
                        break
                    del added_step[key]

            # No filter, add it
            if ok_to_add:
                out.append(added_step)

        return out

    def build(self, python_versions: List[str], command: str, images: List[str], build_steps: List[Dict[str, str]], publish_steps: List[Dict[str, str]]):
        # Create directory and build from template
        self.main_output.parent.mkdir(parents=True, exist_ok=True)
        self.build_from_template(
            self.main_input,
            self.main_output,
            {
                "pythonVersions": python_versions,
                "command": command,
                "images": images,
                "buildExtraSteps": self.filter_steps(build_steps),
                "publishExtraSteps": self.filter_steps(publish_steps),
            },
        )


class PythonVersionsResolver(NmkListConfigResolver):
    def get_value(self, name: str) -> List[str]:
        # If "manual" configuration is provided
        gh_versions = self.model.config["githubPythonVersions"].value
        if len(gh_versions):
            return gh_versions

        # If python plugin is present
        if "pythonSupportedVersions" in self.model.config:
            return self.model.config["pythonSupportedVersions"].value

        # Default: no version
        return []
