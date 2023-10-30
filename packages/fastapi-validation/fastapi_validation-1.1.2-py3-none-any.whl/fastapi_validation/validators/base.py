from abc import abstractmethod


class BaseValidator:
    @abstractmethod
    def validate(self, *criterion):
        pass
