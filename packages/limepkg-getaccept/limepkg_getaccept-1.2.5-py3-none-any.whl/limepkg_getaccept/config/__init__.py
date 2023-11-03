import lime_admin.plugins
from .schema import create_schema


class RuntimeConfig(lime_admin.plugins.AdminPlugin):

    @property
    def name(self):
        return 'limepkg_getaccept'

    @property
    def title(self):
        return 'GetAccept eSigning'

    @property
    def version(self):
        return 1

    def get_config(self):
        try:
            return super().get_config()
        except lime_admin.plugins.NotFoundError:
            return {}

    def get_schema(self):
        return create_schema(self.application)

    def set_config(self, config):
        super().set_config(config=config)


def register_config():
    return RuntimeConfig
