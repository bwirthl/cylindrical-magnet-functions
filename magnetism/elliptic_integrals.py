from scipy.special import elliprd as CarlsonRD
from scipy.special import elliprf as CarlsonRF
from scipy.special import elliprj as CarlsonRJ


def EllipticK(m):
    """
    Computes the complete elliptic integral of the first kind.
    """
    return CarlsonRF(0, 1 - m, 1)


def EllipticE(m):
    """
    Computes the complete elliptic integral of the second kind.
    """
    return CarlsonRF(0, 1 - m, 1) - (1 / 3) * m * CarlsonRD(0, 1 - m, 1)


def EllipticPi(n, m):
    """
    Computes the complete elliptic integral of the third kind.
    """
    return CarlsonRF(0, 1 - m, 1) + (1 / 3) * n * CarlsonRJ(0, 1 - m, 1, 1 - n)
