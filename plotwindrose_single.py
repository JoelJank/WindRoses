import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import json
from python.Functions.heightplot import heightplots
from python.Functions.readliteraturewindrosedata import read_literature_windrose_data
from python.Functions.windrose_from_shear import windrose_from_shear


def plot_windrose_on_Ax(ax, data, name ,bin_size = 10):
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title(f"{name})", fontsize = 13, fontweight = "bold")
    width = np.radians(bin_size)
    ax.bar(np.radians(data["Degree"]), data["Length"], 
           width = width, bottom = 0.0, align = "center", edgecolor = "black", linewidth = 0.5, 
           alpha = 1, facecolor = "black")
    ax.set_ylim(0,1)
    ax.set_yticklabels([])


if __name__ == "__main__":
    settingsfile = os.path.join(os.path.dirname(__file__), "settings.json")
    with open (settingsfile, 'r') as f:
        settings = json.load(f)
        
    

    fig, axes = plt.subplots(nrows = 4, ncols = 2, figsize = (settings["figsize"][0]*2, settings["figsize"][1]*4), dpi = 300)
    ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8 = axes.flatten()
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
    ax2.set_title("Heightplot with Windrose of Hobbs et. al.", fontsize = settings["fontsize_plot"])
    
    heightplots(settings["heightfile"], settings["meshgrid_params"],
                                                ax = ax3,
                                                rectangles = settings["rectangles"], 
                                                save_figure = False, 
                                                safepath = None, 
                                                figsize = settings["figsize"], 
                                                colormap = settings["colormap"], 
                                                fontsize_plot = settings["fontsize_plot"], 
                                                fontsize_legends = settings["fontsize_legends"])
    ax3.set_title("0 degree", fontsize = settings["fontsize_plot"])
    
    heightplots(settings["heightfile"], settings["meshgrid_params"],
                                                ax = ax4,
                                                rectangles = settings["rectangles"], 
                                                save_figure = False, 
                                                safepath = None, 
                                                figsize = settings["figsize"], 
                                                colormap = settings["colormap"], 
                                                fontsize_plot = settings["fontsize_plot"], 
                                                fontsize_legends = settings["fontsize_legends"])
    ax4.set_title("45 degree", fontsize = settings["fontsize_plot"])
    
    heightplots(settings["heightfile"], settings["meshgrid_params"],
                                                ax = ax5,
                                                rectangles = settings["rectangles"], 
                                                save_figure = False, 
                                                safepath = None, 
                                                figsize = settings["figsize"], 
                                                colormap = settings["colormap"], 
                                                fontsize_plot = settings["fontsize_plot"], 
                                                fontsize_legends = settings["fontsize_legends"])
    ax5.set_title("90 degree", fontsize = settings["fontsize_plot"])
    
    heightplots(settings["heightfile"], settings["meshgrid_params"],
                                                ax = ax6,
                                                rectangles = settings["rectangles"], 
                                                save_figure = False, 
                                                safepath = None, 
                                                figsize = settings["figsize"], 
                                                colormap = settings["colormap"], 
                                                fontsize_plot = settings["fontsize_plot"], 
                                                fontsize_legends = settings["fontsize_legends"])
    ax6.set_title("180 degree", fontsize = settings["fontsize_plot"])
    
    heightplots(settings["heightfile"], settings["meshgrid_params"],
                                                ax = ax7,
                                                rectangles = settings["rectangles"], 
                                                save_figure = False, 
                                                safepath = None, 
                                                figsize = settings["figsize"], 
                                                colormap = settings["colormap"], 
                                                fontsize_plot = settings["fontsize_plot"], 
                                                fontsize_legends = settings["fontsize_legends"])
    ax7.set_title("315 degree", fontsize = settings["fontsize_plot"])

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
            plot_windrose_on_Ax(inset_ax, data_dict[name], name, bin_size = settings["winddir_binsize"])
            
    shearstressdata = "Data/shearstressdata_05"
    axes = [ax3, ax4, ax5, ax6, ax7]
    winddirection = [0, 45, 90, 180, 315]
    params = settings["meshgrid_params"]
    meshgrid_params = (
    params["x_min"],
    params["x_max"],
    params["y_min"],
    params["y_max"],
    params["x_step"],
    params["y_step"]
)
    i = 0
    for filename in sorted(os.listdir(shearstressdata)):
        if filename.endswith('_nodevalues_taux.npy'):
            taux = os.path.join(shearstressdata, filename)
            tauy = taux.replace("taux", "tauy")
            data_dict = windrose_from_shear(taux, tauy, meshgrid_params, settings["rectangles"], 
                                            removecharactersfromfilename = ["v_0.5_","_nodevalues_taux"], 
                                            winddir_binsize = settings["winddir_binsize"], 
                                            bin_size = settings["winddir_binsize"])
            for field in dunefields_info:
                region = field["name"]
                x_pos, y_pos = field["rose_position"]
                inset_ax = axes[i].inset_axes([x_pos - rose_size / 2,
                                       y_pos - rose_size / 2,
                                       rose_size, rose_size],
                                       transform = axes[i].transData,
                                       projection = 'polar')
                plot_windrose_on_Ax(inset_ax, data_dict[region], region, bin_size = settings["winddir_binsize"])
                axes[i].set_title(f"{winddirection[i]} degree", fontsize = settings["fontsize_plot"])
            i += 1
    ax8.axis('off')

    
    plt.savefig("singleplots_v05.png", dpi = 300, bbox_inches = "tight")
    