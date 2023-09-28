from scipy.special import elliprd as CarlsonRD
from scipy.special import elliprf as CarlsonRF
from scipy.special import elliprj as CarlsonRJ


def EllipticK(m):
    """
    Computes the complete elliptic integral of the first kind.
    """
    # Remove singularity at m = 1
    if m == 1:
        m = 1 - 1e-9
    return CarlsonRF(0, 1 - m, 1)


def EllipticE(m):
    """
    Computes the complete elliptic integral of the second kind.
    """
    # Remove singularity at m = 1
    if m == 1:
        m = 1 - 1e-9
    return CarlsonRF(0, 1 - m, 1) - (1 / 3) * m * CarlsonRD(0, 1 - m, 1)


def EllipticPi(n, m):
    """
    Computes the complete elliptic integral of the third kind.
    """
    # Remove singularity at m = 1 and n = 1
    if m == 1:
        m = 1 - 1e-9
    if n == 1:
        n = 1 - 1e-9
    return CarlsonRF(0, 1 - m, 1) + (1 / 3) * n * CarlsonRJ(0, 1 - m, 1, 1 - n)
