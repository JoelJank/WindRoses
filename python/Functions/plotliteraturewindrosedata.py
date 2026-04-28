import matplotlib.pyplot as plt
import numpy as np
from readliteraturewindrosedata import read_literature_windrose_data


def plot_literature_windrose_data(folder_path, bin_size = 10, save_fig = False, save_path = None):
    """
    Plots wind rose data from .dat files in the specified folder.

    Parameters:
    folder_path (str): The absolute path to the folder containing the .csv files. The files need to contain: Degree (starting degree of the bin), x (x Position of the end of the bin), y (y Position of the end of the bin). The files need to be separated by ';' and use ',' as decimal separator.
    bin_size (int, optional): The size of the bins in degrees. Default is 10.
    save_fig (bool, optional): Whether to save the figure as PNG files. Default is False.
    save_path (str, optional): The absolute path to the directory where the figure should be saved. If None, the figure will be saved in the current working directory.
    
    Returns:
    dict: A dictionary where keys are file names and values are tuples of (figure, axes) for each wind rose plot.
    """
    names, data_dict = read_literature_windrose_data(folder_path, bin_size)

    plots_dict = {}
    
    for name in names:
        df = data_dict[name]
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        width = np.radians(bin_size)
        bars = ax.bar(np.radians(df["Degree"]), df["Length"], width = width, bottom = 0.0, align = "center", edgecolor = "black", linewidth = 0.5, alpha = 1, facecolor = "black")
        ax.set_ylim(0,1)
        ax.set_yticks(np.arange(0, 1, 0.2))
        ax.set_yticklabels(["0", "20", "40", "60", "80"])
        if save_fig:
            if save_path:
                plt.savefig(save_path + f"/{name}_windrose.png", dpi = 300, bbox_inches = "tight")
            else:
                plt.savefig(f"{name}_windrose.png", dpi = 300, bbox_inches = "tight")
        
        plots_dict[name] = (fig,ax)

    return plots_dict