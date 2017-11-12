"""Minor utils."""


def extract_by_key(scopes):
    """Restructure initial scope dict into vendor baaed indexing.

    >>> received= extract_by_key({'age': ['key1', 'key2'], 'location': ['key1']})
    >>> expected = {'key1': ['age', 'location'], 'key2': ['age']}
    >>> sorted(received.items(), key=lambda t: t[1]) \
== sorted(expected.items(), key=lambda t: t[1])
    True
    """
    keys = {}

    for scope in scopes:

        for key in scopes[scope]:
            if key not in keys:
                keys[key] = []

            keys[key].append(scope)

    return keys
