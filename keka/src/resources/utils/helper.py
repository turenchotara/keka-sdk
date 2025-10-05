from typing import Any, Tuple


def check_next_page(data: dict[str, Any]) -> Tuple[bool, str]:
    """
    This function checks if the next page of data is available.
    :param data:
    :return:
    """
    if data['nextPage'] is not None:
        return True, data['nextPage']
    else:
        return False, ""