""" Tests various hill shading algorithms

Matplotlib shading
    http://matplotlib.org/examples/pylab_examples/shading_example.html?highlight=codex%20shade


Ran Novitsky
    http://rnovitsky.blogspot.nl/2010/04/using-hillshade-image-as-intensity.html

TODO: look at
    (http://reference.wolfram.com/mathematica/ref/ReliefPlot.html)
    or Generic Mapping Tools
    (http://gmt.soest.hawaii.edu/gmt/doc/gmt/html/GMT_Docs/node145.html)
    
For a list of colormaps:
    http://matplotlib.org/examples/color/colormaps_reference.html
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LightSource

from mpl_toolkits.axes_grid1 import make_axes_locatable

from novitsky import set_shade, hillshade

DEF_AZI = 210.0 # default azimuth angle in degrees
#DEF_AZI = 315.0 # default azimuth angle in degrees
DEF_ALT = 45.0  # default elevation angle in degrees
DEF_SCALE = 10.0

def no_shading(fig, axes, data, cmap):
    " Shows data without hill shading"

    image = axes.imshow(data, cmap)
    axes.set_title('No shading')
    axes.set_xticks([])
    axes.set_yticks([])
    
    divider = make_axes_locatable(axes)    
    colorbar_axes = divider.append_axes('right', size="5%", pad=0.25, add_to_figure=True)
    colorbar = fig.colorbar(image, cax=colorbar_axes, orientation='vertical')


def mpl_hill_shading(fig, axes, data, cmap, azdeg=DEF_AZI, altdeg=DEF_ALT):
    " Shows data matplotlibs implementation of hill shading"
    ls = LightSource(azdeg=azdeg, altdeg=altdeg)
    rgb = ls.shade(data, cmap=cmap)
    
    norm = mpl.colors.Normalize(vmin=np.min(data), vmax=np.max(data))
    
    # Norm will not be used to normalize rgb in in the imshow() call but 
    # is used to normalize the color bar. An alternative is to use ColorbarBase
    # as is demonstrated in novitsky_hill_shading below.
    image = axes.imshow(rgb, cmap, norm=norm)
    axes.set_title('Matplotlib hill shading')
    axes.set_xticks([])
    axes.set_yticks([])    
    
    divider = make_axes_locatable(axes)    
    colorbar_axes = divider.append_axes('right', size="5%", pad=0.25, add_to_figure=True)
    colorbar = fig.colorbar(image, cax=colorbar_axes, orientation='vertical')
    

def novitsky_hill_shading(fig, axes, data, cmap, 
                          azdeg=DEF_AZI, altdeg=DEF_ALT, scale = DEF_SCALE):
    " Shows data with hill shading by Ran Novitsky"

    norm = mpl.colors.Normalize(vmin=np.min(data), vmax=np.max(data))
    
    rgb = set_shade(data, cmap=cmap, azdeg=azdeg, altdeg=altdeg, scale = scale)
    image = axes.imshow(rgb)

    axes.set_title('Ran Novitsky hill shading')
    axes.set_xticks([])
    axes.set_yticks([])    
    
    divider = make_axes_locatable(axes)    
    colorbar_axes = divider.append_axes('right', size="5%", pad=0.25, add_to_figure=True)
    colorbar = mpl.colorbar.ColorbarBase(colorbar_axes, cmap=cmap, norm=norm, orientation='vertical')


def novitsky_intensity(fig, axes, data, cmap, 
                          azdeg=DEF_AZI, altdeg=DEF_ALT, scale = DEF_SCALE):
    " Shows only the shading component of the shading by Ran Novitsky"
    # Intensity will always be between 0 and 1
    intensity = hillshade(data, azdeg=azdeg, altdeg=altdeg, scale = scale)
    image = axes.imshow(intensity, cmap)

    axes.set_title('Ran Novitsky intensity')
    axes.set_xticks([])
    axes.set_yticks([])    
    
    divider = make_axes_locatable(axes)    
    colorbar_axes = divider.append_axes('right', size="5%", pad=0.25, add_to_figure=True)
    colorbar = fig.colorbar(image, cax=colorbar_axes, orientation='vertical')


def main():
    # test data
    x, y = np.mgrid[-5:5:0.05, -5:5:0.05]
    data = np.sqrt(x ** 2 + y ** 2) + np.sin(x ** 2 + y ** 2)
    #cmap = plt.cm.rainbow
    cmap = plt.cm.cool
    
    # shade data, creating an rgb array.
    
    fig, axes_list = plt.subplots(2, 2, figsize=(12, 12))
    
    if 1:
        no_shading           (fig, axes_list[0, 0], data, cmap)
        mpl_hill_shading     (fig, axes_list[0, 1], data, cmap)
        novitsky_hill_shading(fig, axes_list[1, 0], data, cmap, scale = 0.1)
        novitsky_intensity   (fig, axes_list[1, 1], data, plt.cm.gist_gray, scale = 0.1)
    else:
        novitsky_intensity   (fig, axes_list[0, 0], data, plt.cm.gist_gray, scale = 0.1)
        novitsky_intensity   (fig, axes_list[0, 1], data, plt.cm.gist_gray, scale = 0.2)
        novitsky_intensity   (fig, axes_list[1, 0], data, plt.cm.gist_gray, scale = 0.5)
        novitsky_intensity   (fig, axes_list[1, 1], data, plt.cm.gist_gray, scale = 0.001)

    fig.show()

if __name__ == "__main__":
    main()
    raw_input('please press enter\n')
    