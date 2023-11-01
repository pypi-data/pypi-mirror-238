import humanize


def easy(bites: int) -> str:
    return humanize.naturalsize(bites, binary=True)

