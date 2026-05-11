import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
import json


#v = 0.5 vmin = 0-003, vmax = 0.006
#v = 2 : vmin = -0.05, vmax = 0.075
def velmagplot(taux, tauy, meshgrid_params,  vmin = None, vmax = None, velo = False, ax = None, rectangles = None, save_figure = False, safepath = None, 
                figsize = (10,8), colormap = 'turbo', fontsize_plot = 10, fontsize_legends = 12):
    """
    Reads height data from .npy files in the specified folder.

    Parameters:
    heightfile (str): The absolute path to the .npy file containing the height data.
    meshgrid_params (tuple): A tuple containing the parameters for the meshgrid: (x_start, x_end, y_start, y_end, stepsize_x, stepsize_y).
    rectangles (str, optional): The absolute path to a .json file containing the dimensions and text positions of rectangles to highlight specific regions.
    save_figure (bool, optional): Whether to save the figure as PNG files. Default is False.
    safepath (str, optional): The absolute path to the directory where the figure should be saved. If None, the figure will be saved in the current working directory.
    figsize (tuple, optional): Size of the figure in inches (width, height). Default is (10, 8).
    colormap (str, optional): Colormap to be used for the height plot. Default is 'turbo'.
    fontsize_plot (int, optional): Font size for the colorbar label. Default is 10.
    fontsize_legends (int, optional): Font size for the rectangle labels. Default is 12.

    Returns:
    tuple: A tuple containing the figure and axes objects.
    """

    tauxdf = np.load(taux)
    tauydf = np.load(tauy)

    x_start = meshgrid_params["x_min"]
    x_end = meshgrid_params["x_max"]
    y_start = meshgrid_params["y_min"]
    y_end = meshgrid_params["y_max"]
    stepsize_x = meshgrid_params["x_step"]
    stepsize_y = meshgrid_params["y_step"]

    xq, yq = np.meshgrid(np.arange(x_start, x_end+1, stepsize_x), 
                         np.arange(y_start, y_end+1, stepsize_y))
    
    maentau = np.mean(np.sqrt(tauxdf**2 + tauydf**2))
    
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, dpi=300)
    else:
        fig = ax.get_figure()
    
    if velo: # u = sqrt(tau/rho) with rho = 0.019 for Mars and tau = sqrt(taux^2 + tauy^2)
        if vmin is not None and vmax is not None:
            p = ax.pcolormesh(xq, yq, ((np.sqrt(tauxdf**2 + tauydf**2)/0.019))**(1/2)-(maentau/0.019)**(1/2), shading='auto', cmap=colormap,
                            vmin = np.sign(vmin)*(np.abs(vmin)/0.019)**(1/2), vmax = np.sign(vmax)*(np.abs(vmax)/0.019)**(1/2))
        else:
            p = ax.pcolormesh(xq, yq, ((np.sqrt(tauxdf**2 + tauydf**2)/0.019))**(1/2)-(maentau/0.019)**(1/2), 
                              shading='auto', cmap=colormap)
    else:
        if vmin is not None and vmax is not None:
            p = ax.pcolormesh(xq, yq, (np.sqrt(tauxdf**2 + tauydf**2))-maentau, shading='auto', cmap=colormap,
                            vmin = vmin, vmax = vmax)
        else:
            p = ax.pcolormesh(xq, yq, (np.sqrt(tauxdf**2 + tauydf**2))-maentau, shading='auto', cmap=colormap)

    if rectangles is not None:
        with open(rectangles, 'r') as f:
            rect_pos = json.load(f)
        for rect in rect_pos:
            ax.add_patch(Rectangle((rect['dimensions'][0], rect['dimensions'][1]), 
                                rect['dimensions'][2], rect['dimensions'][3], 
                                fill=False, edgecolor='black', linewidth=2))
            ax.text(rect['textpos'][0], rect['textpos'][1], f"{rect['name']})", fontsize = fontsize_legends, color = 'black')

    cbar = plt.colorbar(p, ax = ax)
    if velo:
        cbar.set_label(r"$\sqrt{(|\tau| - |\tau|_{mean}|)/\rho}$ [m/s]", fontsize = fontsize_plot)
    else:
        cbar.set_label(r"$|\tau| - |\tau|_{mean}$ [Pa]", fontsize = fontsize_plot)
    ax.set_aspect('equal', adjustable = 'box')
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