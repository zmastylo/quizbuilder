"""Simple utilities."""


def first_item(iterable):
    """Given iterable get first element or None if
    empty iterator."""

    return next(iter(iterable or []), None)


def get_query_params(title: str, description: str, owner_email: str):
    query_params = {}

    if title:
        query_params["title__icontains"] = title
    if description:
        query_params["description__icontains"] = description
    if owner_email:
        query_params["owner"] = owner_email

    return query_params
