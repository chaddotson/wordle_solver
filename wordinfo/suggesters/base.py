from functools import cached_property


class Suggester(object):
    """
    Base class for all suggesters.
    """
    @cached_property
    def name(self):
        if hasattr(self, '__pretty_name__'):
            return self.__pretty_name__.format(**self.__dict__)
        return self.__class__.__name__

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        raise NotImplementedError()
