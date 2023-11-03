"""
SAAO telescope info
"""


# third-party
import numpy as np
from astropy.coordinates import EarthLocation

# local
from recipes.dicts import invert
from recipes.oo.slots import SlotHelper

# relative
from .config import CONFIG


# ---------------------------------------------------------------------------- #
# names
METRIC_NAMES = ('1.9m', '1.0m')
IMPERIAL_NAMES = ('74in', '40in')
_prefer_metric = CONFIG.preferences.metric_names

NAME_EQUIVALENTS = _REMAPPED_NAMES = \
    dict(zip(*(IMPERIAL_NAMES, METRIC_NAMES)[::(-1, 1)[_prefer_metric]]))
_INV_NAMES = invert(_REMAPPED_NAMES)
_74, _40 = _INV_NAMES
NAME_EQUIVALENTS.update(
    {'74': _74, '1.9': _74,
     '40': _40, '1.0': _40, '1': _40}
)
KNOWN_NAMES = sorted([*METRIC_NAMES, *IMPERIAL_NAMES, *NAME_EQUIVALENTS])


FOV_REDUCED = {'74':    (2.79, 2.79)}  # with focal reducer


# ---------------------------------------------------------------------------- #

def get_tel(name, metric=_prefer_metric):
    """
    Get standardized telescope name from description.

    Parameters
    ----------
    name : str or int
        Telescope name (see Examples).

    Returns
    -------
    str
        Standardized telescope name.

    Examples
    --------
    >>> get_tel(74)
    '1.9m'
    >>> get_tel(1.9)
    '1.9m'
    >>> get_tel('1.9 m', metric=False)
    '74in'
    >>> get_tel(1)
    '1.0m'
    >>> get_tel('40     in')
    '1.0m'
    >>> get_tel('LESEDI')
    'lesedi'

    Raises
    ------
    ValueError
        If name is unrecognised.
    """

    # sanitize name:  strip "units" (in,m), lower case
    nr = str(name).rstrip('inm ').lower()

    if nr not in KNOWN_NAMES:
        raise ValueError(f'Telescope name {name!r} not recognised. Please '
                         f'use one of the following\n: {KNOWN_NAMES}')

    name = NAME_EQUIVALENTS.get(nr, name)
    return name if metric == _prefer_metric else _INV_NAMES[name]


def get_fov(telescope, unit='arcmin', focal_reducer=False):
    """
    Get telescope field of view

    Parameters
    ----------
    telescope
    focal_reducer
    unit

    Returns
    -------

    Examples
    --------
    >>> get_fov(1)               # 1.0m telescope
    >>> get_fov(1.9)             # 1.9m telescope
    >>> get_fov(74)              # 1.9m
    >>> get_fov('74in')          # 1.9m
    >>> get_fov('40 in')         # 1.0m
    """

    telescope = get_tel(telescope)
    fov = (FOV_REDUCED if focal_reducer else FOV)[telescope]

    # at this point we have the FoV in arcmin
    # resolve units
    if unit in ('arcmin', "'"):
        factor = 1
    elif unit in ('arcsec', '"'):
        factor = 60
    elif unit.startswith('deg'):
        factor = 1 / 60
    else:
        raise ValueError(f'Unknown unit {unit}')

    return np.multiply(fov, factor)

# ---------------------------------------------------------------------------- #


class Telescope(SlotHelper):

    __slots__ = {'name': 'Telescope name',
                 'fov': 'Field of view in arcmin',
                 'loc': 'GPS location'}

    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self.loc = EarthLocation.from_geodetic(*self.loc)


class TelInfo(dict):
    def __getitem__(self, key):
        return super().__getitem__(get_tel(key))


info_dict = {
    # name: fov (arcmin), GPS lat   lon         alt
    _74:      ((1.29, 1.29), (20.81167, -32.462167, 1822)),
    _40:      ((2.85, 2.85), (20.81,    -32.379667, 1810)),
    'lesedi': ((5.7, 5.7),   (20.8105,  -32.379667, 1811))
    # 'salt': ((),  (20.810808, -32.375823, 1798))
}


tel_info = TelInfo({
    name: Telescope(name, *data) for name, data in info_dict.items()
})

# ---------------------------------------------------------------------------- #
