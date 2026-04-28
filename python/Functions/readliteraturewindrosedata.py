import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def read_literature_windrose_data(folder_path, bin_size = 10):
    """
    Reads wind rose data from .dat files in the specified folder. 
    It calculates the length of the bins from the x and y positions and adjusts the degree to represent the center of the bin.

    Parameters:
    folder_path (str): The absolute path to the folder containing the .csv files. The files need to contain: Degree (starting degree of the bin), x (x Position of the end of the bin), y (y Position of the end of the bin). The files need to be separated by ';' and use ',' as decimal separator.
    bin_size (int, optional): The size of the bins in degrees. Default is 10.

    Returns:
    tuple: A tuple containing a list of file names and a dictionary where keys are file names and values are pandas DataFrames of the data.
    """
    windrose_data = {}

    all_degress = np.arange(0,360,bin_size) + bin_size / 2
    
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.csv'):
            prefix = filename.split('_')[0]
            file_path = os.path.join(folder_path, filename)
            data = pd.read_csv(file_path, 
                               header = None, 
                               sep = ';', 
                               decimal = ",", 
                               names = ["Degree", "x", "y"])
            data["Degree"] = data["Degree"] + bin_size / 2
            data["Length"] = np.sqrt(data["x"]**2 + data["y"]**2)
            data.drop(columns=["x", "y"], inplace=True)

            full_data = pd.DataFrame({"Degree": all_degress})

            full_data = full_data.merge(data, on = "Degree", how = "left")
            full_data["Length"].fillna(0, inplace=True)

            if prefix not in windrose_data:
                windrose_data[prefix] = full_data
            else:
                windrose_data[prefix]["Length"] += full_data["Length"]

            for prefix in windrose_data:
                max_length = windrose_data[prefix]["Length"].max()
                if max_length > 0:
                    windrose_data[prefix]["Length"] = windrose_data[prefix]["Length"] / max_length
            
    return list(windrose_data.keys()), windrose_data

