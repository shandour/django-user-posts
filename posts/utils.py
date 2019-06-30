from .constants import REACTION_STATUSES


def process_reaction(post, reaction, user):
    if reaction not in REACTION_STATUSES.values():
        raise Exception(
            'Only reactions in '
            f'{", ".join(REACTION_STATUSES.values())} accepted.')

    if reaction == REACTION_STATUSES.LIKE.value:
        post.upvoted_by.add(user)
        post.downvoted_by.remove(user)
    else:
        post.upvoted_by.remove(user)
        post.downvoted_by.add(user)
