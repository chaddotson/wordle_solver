from functools import cached_property


class Suggester(object):
    @cached_property
    def name(self):
        if hasattr(self, '__pretty_name__'):
            return self.__pretty_name__
        return self.__class__.__name__
