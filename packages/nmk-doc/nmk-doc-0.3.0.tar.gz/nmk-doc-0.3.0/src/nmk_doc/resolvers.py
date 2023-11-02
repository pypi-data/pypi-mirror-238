"""
Module containing all config item resolvers for **nmk-doc** plugin.
"""
import re
from datetime import date

from nmk.model.resolver import NmkIntConfigResolver, NmkStrConfigResolver
from nmk_base.resolvers import FilesResolver

DOC_INCREMENT_PATTERN = re.compile("[0-9.]+")
"""
Document version increment verification pattern
"""


class NmkDocInputsResolver(FilesResolver):
    """
    Resolves all files in doc folder
    """

    @property
    def folder_config(self) -> str:
        """
        Tells **FilesResolver** to search files in **${docPath}** config item.
        """
        return "docPath"


class NmkDocVersionResolver(NmkStrConfigResolver):
    """
    Documentation version resolver
    """

    def get_value(self, name: str) -> str:
        """
        Get resolved version value.
        Behavior of the version resolution is:
          * take git version (see **${gitVersion}** config item description)
          * if this is a tagged version, simply use it
          * otherwise deduce last tag and increment it with increment configured in **${docVersionIncrement}** config item

        :param name: config item name to be resolved
        :return: resolved version
        """

        # Get git version
        git_version = self.model.config["gitVersion"].value

        # Check git version segments
        segments = git_version.split("-")
        doc_version = segments[0]
        if len(segments) == 1:
            # This is a tagged version: use it directly
            return doc_version

        # Not on a tagged version: let's predict the next one with provided increment
        increment = self.model.config["docVersionIncrement"].value
        assert DOC_INCREMENT_PATTERN.match(increment) is not None, f"Invalid docVersionIncrement format: {increment}"

        # Build predicted version
        doc_version_digits = [int(i) for i in doc_version.split(".")]
        increment_digits = [int(i) for i in increment.split(".")]
        assert len(doc_version_digits) == len(
            increment_digits
        ), f"Not the same digits count between version deduced from gitVersion ({doc_version}) and docVersionIncrement ({increment})"
        out_string = ""
        increment_found = False
        for d1, d2 in zip(doc_version_digits, increment_digits):
            # One more digit
            if len(out_string):
                out_string += "."

            # Increment?
            if d2 > 0:
                # Incremented digit found: do it
                out_string += str(d1 + d2)
                increment_found = True
            elif not increment_found:
                # Incremented digit not found yet: just keep original digit
                out_string += str(d1)
            else:
                # Post-increment digit: set them all to 0
                out_string += "0"

        return out_string


class NmkDocYearResolver(NmkIntConfigResolver):
    """
    Current year resolver
    """

    def get_value(self, name: str) -> int:
        """
        Get today's year.

        :param name: config item name to be resolved
        :return: current year
        """

        # Today's year
        return date.today().year
