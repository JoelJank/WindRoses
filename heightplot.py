import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
import json
from pathlib import Path


def heightplots(heightfile, meshgrid_params, rectangles = None, save_figure = False, safepath = None, 
                figsize = (10,8), colormap = 'turbo', fontsize_plot = 10, fontsize_legends = 12):
    """
    Give out the height plot of the area. The height data should be in a .npy file, which can be created from the .dat file using prepdata.py.    
    :param heightfile: Absolute path to the .npy file containing the height data.
    :param meshgrid_params: A tuple containing the parameters for the meshgrid: (x_start, x_end, y_start, y_end, stepsize_x, stepsize_y).
    :param rectangles: Absolute path to a .json file containing the dimensions and text positions of rectangles to highlight specific regions.
    :param save_figure: Whether to save the figure as PNG files.
    :param safepath: Absolute path to the directory where the figure should be saved. If None, the figure will be saved in the current working directory.
    :param figsize: Size of the figure in inches (width, height).
    :param colormap: Colormap to be used for the height plot. Default is 'turbo'.
    :param fontsize_plot: Font size for the colorbar label. Default is 10.
    :param fontsize_legends: Font size for the rectangle labels. Default is 12.
    """

    Aheight = np.load(heightfile)

    x_start, x_end, y_start, y_end, stepsize_x, stepsize_y = meshgrid_params

    xq, yq = np.meshgrid(np.arange(x_start, x_end+1, stepsize_x), 
                         np.arange(y_start, y_end+1, stepsize_y))
    
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    p = ax.pcolormesh(xq, yq, Aheight, shading='auto', cmap=colormap)

    if rectangles is not None:
        with open(rectangles, 'r') as f:
            rect_pos = json.load(f)
        for rect in rect_pos:
            ax.add_patch(Rectangle((rect['dimensions'][0], rect['dimensions'][1]), 
                                rect['dimensions'][2], rect['dimensions'][3], 
                                fill=False, edgecolor='black', linewidth=2))
            ax.text(rect['textpos'][0], rect['textpos'][1], rect['name'], fontsize = fontsize_legends, color = 'black')

    cbar = plt.colorbar(p)
    cbar.set_label("Elevation [m]", fontsize = fontsize_plot)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(xq.min(), xq.max())
    ax.set_ylim(yq.min(), yq.max())


    if save_figure:
        if not safepath:
            workdir = os.getcwd()
            """
            plt.savefig(os.path.join(workdir, 'heightplot.svg'), format = 'svg', 
                        bbox_inches = 'tight', pad_inches = 0, dpi = 300)
            plt.savefig(os.path.join(workdir, 'heightplot.pdf'), format = 'pdf',
                        bbox_inches = 'tight', pad_inches = 0, dpi = 300)
            """
            plt.savefig(os.path.join(workdir, 'heightplot.png'), format = 'png',
                        bbox_inches = 'tight', pad_inches = 0, dpi = 300)
        else:
            """
            plt.savefig(os.path.join(safepath, 'heightplot.svg'), format = 'svg', 
                        bbox_inches = 'tight', pad_inches = 0, dpi = 300)
            plt.savefig(os.path.join(safepath, 'heightplot.pdf'), format = 'pdf',
                        bbox_inches = 'tight', pad_inches = 0, dpi = 300)
            """
            plt.savefig(os.path.join(safepath, 'heightplot.png'), format = 'png',
                        bbox_inches = 'tight', pad_inches = 0, dpi = 300)


    return fig, ax


test1, test2 = heightplots("/home/joel/Schreibtisch/Github/WindRoses/v_2_height.npy", 
                           (-80000, 85000, -85000, 80000, 25, 25), 
                           rectangles = "/home/joel/Schreibtisch/Github/WindRoses/dunefields.json", 
                           save_figure = True, 
                           safepath = "/home/joel/Schreibtisch/Github/WindRoses/figures", 
                           figsize = (10,8), colormap = 'turbo', 
                           fontsize_plot = 10, fontsize_legends = 12)