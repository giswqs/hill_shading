""" Demonstrates basic use of the hill_shade function.
"""
from __future__ import print_function
from __future__ import division

import numpy as np
import matplotlib as mpl

mpl.interactive(False) 
import matplotlib.pyplot as plt

from plotting import make_test_data, add_colorbar
from hillshade import hill_shade

def main():
    fig, axes = plt.subplots(1, 1) 
    fig.tight_layout()

    data = make_test_data('hills')  # 200x200 km. Height between -8.5 and 7.5 km
    print("data range: {} {}".format(np.min(data), np.max(data)))
    
    cmap_name = 'gist_earth'
    cmap=plt.cm.get_cmap(cmap_name)
    
    norm = mpl.colors.Normalize()
    
    rgb = hill_shade(data, terrain=data * 5, # scale terrain height to make relief visible 
                     #azimuth=135, elevation=45,       # uncomment to use different values
                     #ambient_weight=2, lamp_weight=5, # uncomment to use different values
                     cmap=cmap, norm=norm)
        
    axes.imshow(rgb, norm=None, origin='lower')
    
    add_colorbar(axes, cmap, norm=norm, label='Terrain height [km]')
    axes.set_xlabel('[km]')
    axes.set_ylabel('[km]')
                                 
    plt.show()

if __name__ == "__main__":
    main()

        
        
    