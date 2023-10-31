from inspect import signature


def method_class(classes: list) -> dict:
    """
    Returns dictionary of methods and classes.
    """
    return {
        method: Class.__name__
        for Class in classes
        for method in dir(Class)
        if not method.startswith("_")
    }


def method_input(globals: dict, method_class: dict) -> dict:
    """
    Returns dictionary of methods and input graph object
    type (G: NetworkX, nkG: Networkit, iG: igraph).
    """
    return {
        m: list(signature(getattr(globals[c], m)).parameters.keys())[0]
        for m, c in method_class.items()
    }
