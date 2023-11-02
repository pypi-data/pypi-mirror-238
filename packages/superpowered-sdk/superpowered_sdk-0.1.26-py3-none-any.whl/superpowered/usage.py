from . import superpowered

def get_total_storage():
    """
    Get the total account storage in bytes, tokens, and percent of free-tier used.

    References:
        ``GET /usage/total_storage``
    """
    args = {
        'method': 'GET',
        'url': f'{superpowered.get_base_url()}/usage/total_storage',
        'auth': superpowered.auth(),
    }
    return superpowered.make_api_call(args)


def get_billable_events(start_timestamp: int = None, end_timestamp: int = None):
    """
    Get the billing events for a given time period.

    Args:
        start_timestamp (int): The start timestamp in seconds since epoch.
        end_timestamp (int): The end timestamp in seconds since epoch.

    References:
        ``GET /usage/billable_events``
    """
    params = {}
    if start_timestamp is not None:
        params['start_timestamp'] = int(start_timestamp)

    if end_timestamp is not None:
        params['end_timestamp'] = int(end_timestamp)

    args = {
        'method': 'GET',
        'url': f'{superpowered.get_base_url()}/usage/billable_events',
        'auth': superpowered.auth(),
        'params': params
    }
    return superpowered.make_api_call(args)


def get_api_logs(start_timestamp: int = None, end_timestamp: int = None):
    """
    Get the API logs for a given time period.

    Args:
        start_timestamp (int): The start timestamp in seconds since epoch. Must be less than 1 day from end_timestamp.
        end_timestamp (int): The end timestamp in seconds since epoch. Must be less than 1 day from start_timestamp.

    References:
        ``GET /usage/api_logs``
    """
    params = {}
    if start_timestamp is not None:
        params['start_timestamp'] = int(start_timestamp)

    if end_timestamp is not None:
        params['end_timestamp'] = int(end_timestamp)

    args = {
        'method': 'GET',
        'url': f'{superpowered.get_base_url()}/usage/api_logs',
        'auth': superpowered.auth(),
        'params': params
    }
    return superpowered.make_api_call(args)