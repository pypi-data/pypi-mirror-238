"""
Python module for **nmk-doc** plugin builders.
"""

from pathlib import Path

from nmk.model.builder import NmkTaskBuilder
from nmk.utils import run_with_logs
from nmk_base.common import TemplateBuilder


class NmkDocConfigBuilder(TemplateBuilder):
    """
    Builder used to generate doc config files
    """

    def build(self, template: str):
        """
        Called by the **doc.config** and **doc.rtd** tasks, to generate the **sphinx** + **Read The Docs** config files

        :param template: Path to the Jinja template to use for generation**
        """

        # Just build from template
        self.build_from_template(Path(template), self.main_output, {})


class NmkDocSphinxBuilder(NmkTaskBuilder):
    """
    Builder used to trigger **sphinx** documentation build
    """

    def build(self, source_folder: str, output_folder: str):
        """
        Called by the **doc.build** task, to build the **sphinx** documentation

        :param source_folder: doc source folder
        :param output_folder: doc output folder
        """

        # Invoke sphinx
        run_with_logs(["sphinx-build", source_folder, output_folder])

        # Touch main output index (for incremental build)
        self.main_output.touch()
