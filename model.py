# Simple Population Growth Model

def population_growth(P0, r, t):
    """
    Exponential population growth model.
    P0: initial population
    r: growth rate (per unit time)
    t: time (same units as r)
    Returns: population at time t
    """
    return P0 * (2.718281828459045 ** (r * t))

if __name__ == "__main__":
    # Example usage
    P0 = 1000  # initial population
    r = 0.05   # growth rate (5% per time unit)
    t = 10     # time units
    print(f"Population after {t} units: {population_growth(P0, r, t):.2f}")
