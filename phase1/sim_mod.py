import math

from phase1.io_mod import generate_requests

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
        The complete state dictionary
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


def simulate_step(state):
    """
    Advances the simulation by 1 time unit (1 minute).

    This function handles:
    - New request generation
    - Expiration of waiting requests
    - Assigning drivers
    - Driver movement
    - Pickups and deliveries
    - Metrics update
    """

    state["t"] += 1 # tidspunktet for simulation 


    # Anvender io-mod function til at generere nye reqs
    generate_requests(
        state["t"],
        state["pending"],
        state["req_rate"],
        state["width"],
        state["height"]

    )



    # Udløbne reqs, der har ventet læmge
    for req in state["pending"]:
        if req["status"] in ("waiting", "assigned"):
            wait_time = state["t"] - req["t"]
            if wait_time > state["timeout"]:
                req["status"] = "expired"
                state["expired"] += 1

    
    # Tildeler ordrer, der venter til tilgængelige drivers
    for driver in state["drivers"]:
        if driver["target_id"] is None:
            #finds the first waiting req
            for req in state["pending"]:
                if req["status"] == "waiting":
                    req["status"] = "assigned"
                    req["driver_id"] = driver["id"]
                    driver["target_id"] = req["id"]
                    driver["tx"], driver["ty"] = req["px"], req["py"]
                    break  #helps assign one req per driver per step


    for driver in state["drivers"]:
        if driver["target_id"] is not None:
            # Finds the req that a certain driver is assigned to
            req = next((r for r in state["pending"] if r["id"] == driver["target_id"]), None)
            if req is None:
                continue

            #Determines movement target: pickup or delivery
            if req["status"] == "assigned":
                target = (req["px"], req["py"])
            else: 
                target = (req["dx"], req["dy"])
            move_driver(driver, target)

 
    # move_driver pg close_enough bliver hjælpefunktioner nederst 

        # Pickup event
        if close_enough(driver, target) and req["status"] == "assigned":
            req["status"] = "picked"
            driver["tx"], driver["ty"] = req["dx"], req["dy"]




        # Delivery event
        elif close_enough(driver, target) and req["status"] == "picked":
            req["status"] = "delivered"
            state["served"] += 1

            # Records wait time
            state["served_waits"].append(state["t"] - req["t"])


            # Driver becomes available again
            driver["target_id"] = None
        




    # metrics for GUI/UI - "served", "expired" og "avg_wait" disse vlrdier skal implementeres og returnere metrics





    #ekstras: hjælpefunktioner - tilføj andet evt., hvis du har lyst


#mangler --- Matematisk bevægelse mod mål beskrivelse: move_driver flytter chaufføren et lille skridt mod et målpunkt (pickup eller delivery).
#- 

def move_driver(driver, target, speed=1.0):
    """
    Moves a driver toward a target position using a constant speed. 
    """

# close_enough: Returnerer True hvis chaufføren er tæt nok på målet.

#mangler lidt mat: Afstandstjek til mål // funktion: Tjekker om chaufføren er tæt nok på målpunktet til at være “ankommet”.
# Tol = 0.5 betyder: hvis chaufføren er mindre end 0.5 enheder fra målet → han er fremme. Må gerne ændres, hvis det er 

def close_enough(driver, target, tol=0.5):
    """
    Returns True if driver is within a close radius of the target.
    """



    # du må gerne rette/ændrer, hvis der er noget 