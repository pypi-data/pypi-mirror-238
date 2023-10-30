from abc import abstractmethod


class PluginServiceInterface:

    @abstractmethod
    def register(self, *args, **kwargs):
        ...

    @abstractmethod
    def logout(self, *args, **kwargs):
        ...
