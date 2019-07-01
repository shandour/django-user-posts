import enum


class REACTION_STATUSES(enum.Enum):
    LIKE = 1
    DISLIKE = 2

    @classmethod
    def values(cls):
        return [str(el.value) for el in cls]
