""" Hill shading implementation for matplotlib

"""
from __future__ import print_function
from __future__ import division

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, cos, sin, gradient, arctan, hypot, arctan2
from matplotlib import cm
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb

DEF_AZIMUTH = 165   # degrees
DEF_ELEVATION = 45  # degrees
DEF_CMAP = plt.cm.gist_earth
    
    
def _replace_nans(array, array_nan_value):
    """ Returns a copy of the array with the nans replaced by nan_value
    """
    finite_array = np.copy(array)
    is_non_finite = np.logical_not(np.isfinite(array)) # TODO: use mask?
    if np.any(is_non_finite):
        finite_array[is_non_finite] = array_nan_value
    return finite_array
    
    
def _create_norm_function(data, vmin, vmax):
    """ Aux function to create a normalization function
    """
    vmin = np.nanmin(data) if vmin is None else vmin
    vmax = np.nanmax(data) if vmax is None else vmax
    return mpl.colors.Normalize(vmin=vmin, vmax=vmax)    
    
    
def hill_shade_hsv(data, terrain=None, 
                   scale_terrain=0.1, azimuth=DEF_AZIMUTH, elevation=DEF_ELEVATION, 
                   cmap=DEF_CMAP, norm_fn=None, vmin=None, vmax=None, 
                   terrain_nan_value=0):
    """ Calculates hillshading
    """
    if terrain is None:
        terrain = data
    
    assert data.ndim == 2, "data must be 2 dimensional"
    assert terrain.shape == data.shape, "{} != {}".format(terrain.shape, data.shape)
    
    finite_terrain = _replace_nans(terrain, terrain_nan_value)
    
    if norm_fn is None:
        norm_fn = _create_norm_function(data, vmin, vmax)

    norm_data = norm_fn(data)
    rgba = cmap(norm_data)
    hsv = rgb_to_hsv(rgba[:, :, :3])

    intensity = calculate_intensity(finite_terrain, scale_terrain=scale_terrain, 
                                    azimuth=azimuth, elevation=elevation)
    hsv[:, :, 2] = intensity
    
    return hsv_to_rgb(hsv)
    
    
def hill_shade_pegtop(data, terrain=None, 
                      scale_terrain=0.1, azimuth=DEF_AZIMUTH, elevation=DEF_ELEVATION, 
                      cmap=DEF_CMAP, norm_fn=None, vmin=None, vmax=None, 
                      terrain_nan_value=0):
    """ Calculates hillshading
    """
    if terrain is None:
        terrain = data
    
    assert data.ndim == 2, "data must be 2 dimensional"
    assert terrain.shape == data.shape, "{} != {}".format(terrain.shape, data.shape)
    
    finite_terrain = _replace_nans(terrain, terrain_nan_value)
    
    if norm_fn is None:
        norm_fn = _create_norm_function(data, vmin, vmax)
    
    intensity = calculate_intensity(finite_terrain, scale_terrain=scale_terrain, 
                                    azimuth=azimuth, elevation=elevation)
    norm_data = norm_fn(data)
    rgba = cmap(norm_data)    
    
    # get rgb of normalized data based on cmap
    rgb = rgba[:, :, :3]
    
    # form an rgb eqvivalent of intensity
    d = intensity.repeat(3).reshape(rgb.shape)
    
    # simulate illumination based on pegtop algorithm.
    return 2 * d * rgb + (rgb ** 2) * (1 - 2 * d)


    
# Same as novitsky hill shading but where the gradient is
# multiplied by the scale instead of divided.

# TODO: rename
def calculate_intensity(terrain, scale_terrain=0.1, 
                        azimuth=DEF_AZIMUTH, elevation=DEF_ELEVATION):
    """ convert data to hillshade based on matplotlib.colors.LightSource class.
      input:
           terrain - a 2-d array of the terrain
           scale - scaling value of the terrain. higher number = higher gradient
           azdeg - where the light comes from: 0 south ; 90 east ; 180 north ;
                        270 west
           altdeg - where the light comes from: 0 horison ; 90 zenith
      output: a 2-d array of normalized hilshade
    """
    # convert alt, az to radians
    az = azimuth * pi / 180.0
    alt = elevation * pi / 180.0
    # gradient in x and y directions
    dx, dy = gradient(terrain * scale_terrain)
    slope = 0.5 * pi - arctan(hypot(dx, dy))
    aspect = arctan2(dx, dy)
    intensity = sin(alt) * sin(slope) + cos(alt) * \
        cos(slope) * cos(-az - aspect - 0.5 * pi)
    intensity = (intensity - intensity.min()) / \
        (intensity.max() - intensity.min())
    return intensity

