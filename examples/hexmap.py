"""Create a basic example hex map using the HexMap class."""
import matplotlib.pyplot as plt
import os
import pandas as pd

from map.hexmap import HexMap
from utils.plotting_utils import create_signature_pc

if __name__ == "__main__":
    map_path = os.path.join("data", "boundaries", "uk_hex.csv")
    data_path = os.path.join("data", "map", "241584", "241584_1553701502.csv")

    map_df = pd.read_csv(map_path, encoding="latin-1")
    data_df = pd.read_csv(data_path, encoding="latin-1")

    hexmapper = HexMap()

    # Create the dataframe containing the map and colour information before loading it
    combined_df = create_signature_pc(map_df, data_df)

    hexmapper.load_map(combined_df, is_path=False, value_column="signature_pc")

    # Draw the map
    v_min = 0.0
    v_max = 35.0
    title = "Signature as % of Electorate"
    title_kwargs = {"fontsize": "20", "fontweight": "6"}
    fig = hexmapper.draw_map(
        v_min=v_min, v_max=v_max, title=title, title_kwargs=title_kwargs
    )
    plt.show()

    # Save the map
    save_dir = os.path.join("plots", "examples")
    hexmapper.save_map("hexmap_example.png", save_dir=save_dir, dpi=300)
