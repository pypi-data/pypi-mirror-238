"""Utilitaires divers pour les calculs"""
import numpy as np


def round_to_closest_multiple(x, m):
    """Return the multiple of m closest to x"""
    return m * np.round(x / m)


def round_to_next_multiple(x, m):
    """Return the ceiling multiple of m from x"""
    return m * np.ceil(x / m)


def round_to_previous_multiple(x, m):
    """Return the flooring multiple of m from x"""
    return m * (x // m)
