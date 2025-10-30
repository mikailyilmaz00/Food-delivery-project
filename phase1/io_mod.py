
def load_drivers(path):
    """
    Load driver positions from a CSV file (no header, only x,y values).
    Skips lines starting with '#'.
    Returns a list of driver dictionaries in the format required by the GUI.
    """
    drivers = []
    with open(path, "r") as f:    # Python åbner filen 
        for line in f:            # Indlæser linje for linje
            line = line.strip()
            # skipper tommer linjer eller kommentarer
            if not line or line.startswith("#"): #her konverteres dataen til tal
                continue

            parts = line.split(",")

            if len(parts) < 2:
                continue

            # konverterer værdier fra tekst til flydende (floats) tal
            x, y = map(float, parts[:2])

            # laver en dictionary for chaufføren
            driver = {
                "id": len(drivers),
                "x": x,
                "y": y,
                "vx": 0.0, "vy": 0.0,   # hastighed - kan ændres senere
                "tx": None, "ty": None, # pick-up/delivery - kan laves senere
                "target_id": None       # tildelt ordre - senere
            }
            drivers.append(driver)

    return drivers

def load_requests(path):
    """
    Reads order data (requests) from a CSV file.
    The format is: time, pickup_x, pickup_y, delivery_x, delivery_y
    Comment lines (starting with '#') are skipped.
    Returns a list of request dictionaries in the project’s required format.
    """

    requests = []  # alle ordres gemmes her

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # spring kommentarer/tomme linjer over

            parts = line.split(",")
            if len(parts) < 5:
                continue  # linjer uden 5 værdier springes over

            # konverterer værdierne til rigtige datatyper
            t, px, py, dx, dy = parts[:5]
            t, px, py, dx, dy = int(float(t)), float(px), float(py), float(dx), float(dy)

            # dictionary for reqs
            req = {
                "id": len(requests),   # id = rækkefølge i filen
                "px": px, "py": py,    # pickup-koordinater
                "dx": dx, "dy": dy,    # dropoff-koordinater
                "t": t,                # tidspunkt ordren blev oprettet
                "t_wait": 0,           # ventetid 
                "status": "waiting",   # startstatus = "venter på tildeling"
                "driver_id": None      # ingen chauffør endnu
            }

            requests.append(req)

    return requests
