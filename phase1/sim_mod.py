def init_state(drivers, requests, timeout, rate, width, height):
    """
    Initializes the full simulation state as described in the project specification (section 4.2.2).

    Parameters
    ----------
    drivers : list[dict]
        List of driver dictionaries (from load_drivers or generate_drivers)
    requests : list[dict]
        List of request dictionaries (from load_requests or generate_requests)
    timeout : int
        Maximum waiting time before a request expires
    rate : float
        Request generation rate (requests per minute)
    width : int
        Width of the simulation grid
    height : int
        Height of the simulation grid

    Returns
    -------
    dict
        The complete state dictionary.
    """
    return {
        "t": 0,                   # starttid
        "drivers": drivers,       # chauffør-liste
        "pending": requests,      # aktuelle ordrer
        "future": [],             # bruges senere hvis I vil udvide projektet
        "served": 0,              # antal leverede ordrer
        "expired": 0,             # antal udløbne ordrer
        "timeout": timeout,       # maks. ventetid
        "served_waits": [],       # ventetider for leverede ordrer
        "req_rate": rate,         # ordrer pr. minut
        "width": width,
        "height": height
    }
