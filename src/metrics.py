# src/metrics.py

def durability_multiplier(l_petro, l_bio):
    """
    Durability multiplier (DM) as defined in thesis:
    DM = L_petro / L_bio
    """
    if l_bio <= 0:
        raise ValueError("Lifetime must be > 0")
    return l_petro / l_bio