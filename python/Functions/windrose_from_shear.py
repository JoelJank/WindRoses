import numpy as np
import matplotlib.pyplot as plt
import os 
from pathlib import Path
import json
import re


def windrose_from_shear(tau_x, tau_y, meshgrid_params, rectangles = None, removecharactersfromfilename = ["v_2_","_nodevalues_taux"], winddir_binsize = 15, bin_size = 10):

    """
    Reads a .npy file of shear stress data and creates a .... containing the data to visualize as a wind rose.

    Parameters:
    tau_x (str): The absolute path to the .npy file containing the x-component of the shear stress data.
    tau_y (str): The absolute path to the .npy file containing the y-component of the shear stress data.
    meshgrid_params (tuple): A tuple containing the parameters for the meshgrid: (x_start, x_end, y_start, y_end, stepsize_x, stepsize_y).
    rectangles (str, optional): The absolute path to a .json file containing the dimensions and text positions of rectangles to highlight specific regions. These rectangles also specify the regions that the wind roses are created for.
    removecharactersfromfilename (str or list, optional): A string or list of strings to remove from the filename to later get the desired wind directions.
    bin_size (int, optional): The size of the bins for the wind rose.

    Returns:

    """
    data_x = np.load(tau_x)
    data_y = np.load(tau_y)

    x_start, x_end, y_start, y_end, stepsize_x, stepsize_y = meshgrid_params

    xq, yq = np.meshgrid(np.arange(x_start, x_end+stepsize_x, stepsize_x), 
                         np.arange(y_start, y_end+stepsize_y, stepsize_y), indexing="xy")
    

    filename = Path(tau_x).stem
    if removecharactersfromfilename:
        if isinstance(removecharactersfromfilename, list):
            for char in removecharactersfromfilename:
                filename = filename.replace(char, '')
        else:
            filename = filename.replace(removecharactersfromfilename, '')

    if int(filename) == 1:
        winddirection = 0
    else:
        winddirection = (int(filename)-1) * winddir_binsize #This is matched for my system: If the nummeration is different, change it

    math_angle = np.degrees(np.arctan2(data_y, data_x))
    wind_from = (270 - math_angle) % 360

    bins = np.arange(0,361,bin_size)
    bin_centers = bins[:-1] + bin_size / 2


    def compute_windrose_for_region(mask):
        hist,_ = np.histogram(wind_from[mask], bins = bins)
        hist_norm = hist / np.max(hist)
        return {

            "Degree": bin_centers,
            "Length": hist_norm.copy(),
            "Counts": hist
        }
    

    windroses = {}
    if rectangles is not None:
        with open(rectangles, 'r') as f:
            rect_pos = json.load(f)
        
        for rect in rect_pos:
            xmin = rect['dimensions'][0]
            xmax = rect['dimensions'][0] + rect['dimensions'][2]
            ymin = rect['dimensions'][1]
            ymax = rect['dimensions'][1] + rect['dimensions'][3]

            mask = (xq >= xmin) & (xq <= xmax) & (yq >= ymin) & (yq <= ymax)


            if np.any(mask):
                windroses[rect['name']] = compute_windrose_for_region(mask)

    return windroses



        
    


    


