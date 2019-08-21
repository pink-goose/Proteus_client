from .configuration import Configuration


class ConfigurationManager(Configuration):
    def instance(self):
        configuration = Configuration()
        configuration.get()
        return configuration.config
