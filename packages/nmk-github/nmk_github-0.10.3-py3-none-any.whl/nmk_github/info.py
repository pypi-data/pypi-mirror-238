import os
import re
import urllib.parse
from typing import Tuple

from nmk.model.resolver import NmkConfigResolver, NmkStrConfigResolver
from nmk.utils import run_with_logs

REMOTE_PATTERN = re.compile("origin[\\t ]+(?:(?:git@)|(?:https://))github.com[:/]([^/]+)/([^.]+)(?:.git)?[\\t ]+\\(fetch\\)")


class GithubRemoteParser(NmkStrConfigResolver):
    def get_remote(self) -> Tuple[str, str]:
        cp = run_with_logs(["git", "remote", "-v"])
        for line in cp.stdout.split("\n"):
            m = REMOTE_PATTERN.match(line)
            if m is not None:
                return (m.group(1), m.group(2))
        raise AssertionError("Failed to parse git fetch remote URL")


class GithubUserResolver(GithubRemoteParser):
    def get_value(self, name: str) -> str:
        user, _ = self.get_remote()
        return user


class GithubRepoResolver(GithubRemoteParser):
    def get_value(self, name: str) -> str:
        _, repo = self.get_remote()
        return repo


class GithubIssuesLabelResolver(NmkStrConfigResolver):
    def get_value(self, name: str) -> str:
        # Check for optional label
        label = self.model.config["githubIssuesLabel"].value
        return "+" + urllib.parse.quote(f"label:{label}") if len(label) else ""


class GithubCIResolver(NmkConfigResolver):
    """
    Resolver for **gitEnableDirtyCheck** config item override
    """

    def get_type(self, name: str) -> object:
        return bool

    def get_value(self, name: str) -> str:
        """
        Resolution logic for **gitEnableDirtyCheck**: check if **CI** env var is defined
        """
        return "CI" in os.environ and (len(os.environ["CI"]) > 0)
