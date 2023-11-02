import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
from volstreet.blackscholes import call, put

N = norm.cdf  # Normal distribution cumulative density function


# Calculate d1 term in Black-Scholes formula
def d1(
    S: np.ndarray, K: np.ndarray, t: np.ndarray, r: np.ndarray, sigma: np.ndarray
) -> np.ndarray:
    numerator = np.log(S / K) + (r + 0.5 * sigma**2) * t
    denominator = sigma * np.sqrt(t)
    return numerator / denominator


# Calculate d2 term in Black-Scholes formula
def d2(
    S: np.ndarray, K: np.ndarray, t: np.ndarray, r: np.ndarray, sigma: np.ndarray
) -> np.ndarray:
    return d1(S, K, t, r, sigma) - sigma * np.sqrt(t)


# Calculate Delta
def delta(
    S: np.ndarray,
    K: np.ndarray,
    t: np.ndarray,
    r: np.ndarray,
    sigma: np.ndarray,
    flag: np.ndarray,
) -> np.ndarray:
    d_1 = d1(S, K, t, r, sigma)
    delta_values = np.zeros_like(d_1)

    put_indices = np.char.startswith(flag, "P")
    call_indices = np.logical_not(put_indices)

    delta_values[put_indices] = N(d_1[put_indices]) - 1.0
    delta_values[call_indices] = N(d_1[call_indices])

    return delta_values


# Calculate Gamma
def gamma(
    S: np.ndarray, K: np.ndarray, t: np.ndarray, r: np.ndarray, sigma: np.ndarray
) -> np.ndarray:
    d_1 = d1(S, K, t, r, sigma)
    return np.exp(-0.5 * d_1**2) / (S * sigma * np.sqrt(2 * np.pi * t))


# Calculate Theta
def theta(
    S: np.ndarray,
    K: np.ndarray,
    t: np.ndarray,
    r: np.ndarray,
    sigma: np.ndarray,
    flag: np.ndarray,
) -> np.ndarray:
    D1 = d1(S, K, t, r, sigma)
    D2 = d2(S, K, t, r, sigma)
    first_term = (-S * np.exp(-0.5 * D1**2) * sigma) / (2 * np.sqrt(2 * np.pi * t))
    theta_values = np.zeros_like(D1)

    call_indices = np.char.startswith(flag, "C")
    put_indices = np.logical_not(call_indices)

    second_term_call = r * K * np.exp(-r * t) * N(D2)
    second_term_put = r * K * np.exp(-r * t) * N(-D2)

    theta_values[call_indices] = (
        first_term[call_indices] - second_term_call[call_indices]
    ) / 365.0
    theta_values[put_indices] = (
        first_term[put_indices] + second_term_put[put_indices]
    ) / 365.0

    return theta_values


# Calculate Vega
def vega(
    S: np.ndarray, K: np.ndarray, t: np.ndarray, r: np.ndarray, sigma: np.ndarray
) -> np.ndarray:
    d_1 = d1(S, K, t, r, sigma)
    return S * np.exp(-0.5 * d_1**2) * np.sqrt(t) / np.sqrt(2 * np.pi) * 0.01


# The implied_volatility function may not be easily vectorizable due to the use of the brentq root-finding method.
# It's best to loop over each element in this case.
def implied_volatility(
    price: np.ndarray,
    S: np.ndarray,
    K: np.ndarray,
    t: np.ndarray,
    r: np.ndarray,
    flag: np.ndarray,
) -> np.ndarray:
    iv = np.zeros_like(price)
    for i in range(len(price)):
        if str(flag[i]).upper().startswith("P"):
            f = lambda sigma: price[i] - put(S[i], K[i], t[i], r[i], sigma)
        else:
            f = lambda sigma: price[i] - call(S[i], K[i], t[i], r[i], sigma)
        try:
            iv[i] = brentq(f, 1e-12, 100, xtol=1e-15, rtol=1e-15, maxiter=1000)
        except ValueError:
            iv[i] = np.nan
    return iv
