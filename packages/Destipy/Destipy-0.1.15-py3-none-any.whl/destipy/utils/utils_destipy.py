def format_param_form_list(content: list, paramName: str):
    """Formats a list of items into a string for use in a request.

    Args:
        list (list): The list of items to be formatted.
        paramName (str): The name of the parameter.

    Returns:
        str: The formatted list as a string.
    """
    params = paramName + "=" + ",".join(content)
    return params
