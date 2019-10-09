import matplotlib.pyplot as plt
import os
import pandas as pd

from map.hexmap import HexMap


def create_signature_pc(map_df, data_df):
    combined_df = (
        map_df.set_index("Constituency").join(data_df.set_index("name")).reset_index()
    )
    combined_df["mp"] = combined_df["mp"].fillna("No MP")
    combined_df["signature_count"] = combined_df["signature_count"].fillna(0)
    combined_df["signature_pc"] = (
        100 * combined_df["signature_count"] / combined_df["Electorate"]
    )
    return combined_df


def plot_batch(data_dir, map_path, save_dir, **draw_map_kwargs):
    assert os.path.exists(data_dir), "{} does not exist".format(data_dir)
    map = HexMap()
    map.save_directory = save_dir

    map_df = pd.read_csv(map_path, encoding="latin-1")

    for r, d, f in os.walk(data_dir):
        for _f in f:
            if ".csv" in _f:
                file_name = os.path.join(r, _f)
                save_name = os.path.join(save_dir, _f.split(".")[0]) + ".png"
                if not os.path.exists(save_name):
                    # Check that you haven't already created this map
                    print("Getting map for {}".format(_f))

                    data_df = pd.read_csv(file_name, encoding="latin-1")
                    combined_df = create_signature_pc(map_df, data_df)

                    map.load_map(
                        combined_df, is_path=False, value_column="signature_pc"
                    )
                    map.draw_map(**draw_map_kwargs)

                    map.save_map(save_name, dpi=300)
                    plt.close()
