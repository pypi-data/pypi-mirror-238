"""New Provider Command."""
import inflection
import os

from ..utils.filesystem import make_directory, render_stub_file, get_module_dir
from ..utils.str import as_filepath
from ..utils.location import base_path
from .Command import Command


class MakeProviderCommand(Command):
    """
    Creates a new provider class.

    provider
        {name : Name of the provider}
        {--f|force=? : Force overriding file if already exists}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))

        content = render_stub_file(self.get_providers_path(), name)

        relative_filename = os.path.join(
            as_filepath(self.app.make("providers.location")), name + ".py"
        )
        filepath = base_path(relative_filename)
        make_directory(filepath)
        if os.path.exists(filepath) and not self.option("force"):
            self.warning(
                f"{filepath} already exists! Run the command with -f (force) to override."
            )
            return -1

        with open(filepath, "w") as f:
            f.write(content)

        # add class to __init__.py
        with open(os.path.join(os.path.dirname(filepath), "__init__.py"), "a") as f:
            f.write(f"from .{name} import {name}\n")

        self.info(f"Provider Created ({relative_filename})")

    def get_providers_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/providers/Provider.py")
