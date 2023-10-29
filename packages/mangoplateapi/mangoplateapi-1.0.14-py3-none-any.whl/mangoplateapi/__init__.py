import logging

from mangoplateapi.mixins.code import CodeMixin
from mangoplateapi.mixins.keyword import KeywordMixin
from mangoplateapi.mixins.restaurant import RestaurantMixin
from mangoplateapi.mixins.review import ReviewMixin
from mangoplateapi.mixins.story import StoryMixin
from mangoplateapi.mixins.theme import ThemeMixin


__VERSION__ = "1.0.14"

DEFAULT_LOGGER = logging.getLogger("mangoplateapi")


class Client(
    CodeMixin,
    RestaurantMixin,
    ReviewMixin,
    StoryMixin,
    ThemeMixin,
    KeywordMixin
):
    pass
