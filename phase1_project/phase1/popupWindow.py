import matplotlib.pyplot as plt
from .io_mod import load_drivers, load_requests
from .sim_mod import init_state, simulate_step

def popupWindow(): 
    drivers = load_drivers("data/drivers.csv")
    requests = load_requests("data/requests.csv")

    state = init_state(
        drivers,
        requests,
        timeout=10,
        rate=0.8,
        width=50,
        height=40
    )

    served_hist = []
    expired_hist = []
    avg_hist = []

    for _ in range(600):
        state, metrics = simulate_step(state)
        served_hist.append(metrics["served"])
        expired_hist.append(metrics["expired"])
        avg_hist.append(metrics["avg_wait"])


    # popup shows after ending of simulation
    plt.ylim(0, 300)
    plt.plot(served_hist, label="served")
    plt.plot(expired_hist, label="expired")
    plt.plot(avg_hist, label="avg_wait" )
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("value")
    plt.show()


if __name__ == "__main__":
    popupWindow()
