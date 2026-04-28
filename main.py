import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "python/Functions"))
from heightplot import heightplots
from readliteraturewindrosedata import read_literature_windrose_data


def plot_windrose_on_Ax(ax, data, bin_size = 10):
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    width = np.radians(bin_size)
    ax.bar(np.radians(data["Degree"]), data["Length"], 
           width = width, bottom = 0.0, align = "center", edgecolor = "black", linewidth = 0.5, 
           alpha = 1, facecolor = "black")
    ax.set_ylim(0,1)


if __name__ == "__main__":
    settingsfile = os.path.join(os.path.dirname(__file__), "settings.json")
    with open (settingsfile, 'r') as f:
        settings = json.load(f)

    fig, (ax1,ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = (settings["figsize"][0]*2, settings["figsize"][1]), dpi = 300)
    
    heightplots(settings["heightfile"], settings["meshgrid_params"],
                                                ax = ax1,
                                                rectangles = settings["rectangles"], 
                                                save_figure = False, 
                                                safepath = None, 
                                                figsize = settings["figsize"], 
                                                colormap = settings["colormap"], 
                                                fontsize_plot = settings["fontsize_plot"], 
                                                fontsize_legends = settings["fontsize_legends"])
    ax1.set_title("Heightplot", fontsize = settings["fontsize_plot"])

    heightplots(settings["heightfile"], settings["meshgrid_params"],
                                                ax = ax2,
                                                rectangles = settings["rectangles"], 
                                                save_figure = False, 
                                                safepath = None, 
                                                figsize = settings["figsize"], 
                                                colormap = settings["colormap"], 
                                                fontsize_plot = settings["fontsize_plot"], 
                                                fontsize_legends = settings["fontsize_legends"])
    ax2.set_title("Heightplot with Windrose", fontsize = settings["fontsize_plot"])

    names, data_dict = read_literature_windrose_data(settings["literature_path"], settings["winddir_binsize"])
    with open(settings["rectangles"], 'r') as f:
        dunefields_info = json.load(f)

    rose_size = settings["rose_inset_size"]
    
    for field in dunefields_info:
        name = field["name"]
        position = field["rose_position"]


        if name in data_dict:
            x_pos, y_pos = position

            inset_ax = ax2.inset_axes([x_pos - rose_size / 2,
                                       y_pos - rose_size / 2,
                                       rose_size, rose_size],
                                       transform = ax2.transData,
                                       projection = 'polar')
            plot_windrose_on_Ax(inset_ax, data_dict[name], bin_size = settings["winddir_binsize"])



    #TODO: Add text with region name under the windroses. 
    #TODO: Fix the inset position of the windroses in the dunefield.json. Fix the size of the inset ticks.


    
    plt.savefig("test.png", dpi = 300, bbox_inches = "tight")
    