import numpy as np
import matplotlib.pyplot as plt
import os
from windrose_from_shear import windrose_from_shear

def plot_own_windrose(folder_path, meshgrid_params, rectangles = None, removecharactersfromfilename = ["v_0.5_","_nodevalues_taux"], winddir_binsize = 15, bin_size = 10, save_fig = False, save_path = None):
    
    plots_dict = {}

    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('_nodevalues_taux.npy'):
            tau_x = os.path.join(folder_path, filename)
            tau_y = tau_x.replace("taux", "tauy")
            print(f"Processing {filename}...")
            dataroses = windrose_from_shear(tau_x, tau_y, 
                                            meshgrid_params, rectangles, 
                                            removecharactersfromfilename, winddir_binsize, 
                                            bin_size)
            winddirection = dataroses['winddirection']
        for regions, data in dataroses['windroses'].items():
            degree, length, counts = data['Degree'], data['Length'], data['Counts']
            fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
            width = np.radians(bin_size)
            bars = ax.bar(np.radians(degree), length, width = width, bottom = 0.0, align = "center", edgecolor = "black", linewidth = 0.5, alpha = 1, facecolor = "black")
            ax.set_ylim(0,1)
            ax.set_yticks(np.arange(0, 1, 0.2))
            ax.set_yticklabels(["0", "20", "40", "60", "80"])
            ax.set_title(f"Winddirection: {winddirection}. Region: {regions}")
            plots_dict[f"{winddirection}_{regions}"] = fig, ax
            if save_fig:
                if save_path:
                    os.makedirs(save_path, exist_ok=True)
                    plt.savefig(os.path.join(save_path, f"{winddirection}_{regions}_windrose.png"), dpi = 300, bbox_inches = "tight")
                else:
                    plt.savefig(f"{winddirection}_{regions}_windrose.png", dpi = 300, bbox_inches = "tight")


    return plots_dict

plot_own_windrose(r"H:\Github\WindRoses\Data\shearstressdata_05", 
                  (-80000, 85000, -85000, 80000, 25, 25), 
                  rectangles = "H:\Github\WindRoses\dunefields.json", save_fig = True, 
                  save_path = r"H:\Github\WindRoses\Figures\ownwindrose_05")

        


        
