from enum import Enum


class Filter(str, Enum):
    """Filters enum, like "$eq" and "$lt".

    Docs:
    https://docs.strapi.io/developer-docs/latest/developer-resources/database-apis-reference/rest/filtering-locale-publication.html#filtering
    """

    eq = '$eq'
    """Equal"""
    ne = '$ne'
    """Not equal"""
    lt = '$lt'
    """Less than"""
    lte = '$lte'
    """Less than or equal to"""
    gt = '$gt'
    """Greater than"""
    gte = '$gte'
    """Greater than or equal to"""
    IN = '$in'
    """Included in an array"""
    notIn = '$notIn'
    """Not included in an array"""
    contains = '$contains'
    """Contains (case-sensitive)"""
    notContains = '$notContains'
    """Does not contain (case-sensitive)"""
    containsi = '$containsi'
    """Contains"""
    notContainsi = '$notContainsi'
    """Does not contain"""
    null = '$null'
    """Is null"""
    notNull = '$notNull'
    """Is not null"""
    between = '$between'
    """Is between"""
    startsWith = '$startsWith'
    """Starts with"""
    endsWith = '$endsWith'
    """Ends with"""
    OR = '$or'
    """Joins the filters in an "or" expression"""
    AND = '$and'
    """Joins the filters in an "and" expression"""


class PublicationState(str, Enum):
    live = 'live'
    """returns only published entries (default)"""
    preview = 'preview'
    """returns both draft entries & published entries"""
