import numpy as np

def prepdata(datfile,savepath, sep = "\t"):
    """
    Reads a .dat file, converts it to a numpy array and saves it as a .npy file.

    Parameters:
    datfile (str): The absolute path to the .dat file containing the data.
    savepath (str): The absolute path where the .npy file will be saved.
    sep (str, optional): The delimiter used in the .dat file. Default is tab ("\t").
    """
    data = np.loadtxt(datfile, delimiter = sep)
    np.save(savepath, data)


tau_x = np.load("/home/joel/Schreibtisch/Github/WindRoses/Data/shearstressdata/v_2_7_nodevalues_taux.npy")
tau_y = np.load("/home/joel/Schreibtisch/Github/WindRoses/Data/shearstressdata/v_2_7_nodevalues_tauy.npy")

# Nimm einen Punkt (z.B. in der Mitte)
mid_x = tau_x.shape[0] // 2
mid_y = tau_y.shape[1] // 2

tx = tau_x[mid_x, mid_y]
ty = tau_y[mid_x, mid_y]

angle_tau = np.degrees(np.arctan2(ty, tx))
wind_from = (angle_tau + 180) % 360

print(f"Punkt ({mid_x}, {mid_y}): tau_x={tx:.4f}, tau_y={ty:.4f}")
print(f"tau-Richtung (Strömungsrichtung): {angle_tau:.1f}°")
print(f"Kommende Windrichtung: {wind_from:.1f}°")

print(f"wind_from shape: {wind_from.shape}")
print(f"wind_from dtype: {wind_from.dtype}")
print(f"Unique Werte in wind_from (erste 20): {np.unique(wind_from)[:20]}")
print(f"Min: {wind_from.min()}, Max: {wind_from.max()}")
print(f"Anzahl NaN: {np.isnan(wind_from).sum()}")



