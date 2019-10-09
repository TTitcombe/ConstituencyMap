from matplotlib.collections import PatchCollection
from matplotlib.patches import RegularPolygon
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd


class HexMap:
    """
    HexMap creates a map by drawing equally sized polygons.
    These maps are useful to visualise election results, as
    metropolitan areas can often distort how many people are
    voting a certain way.
    """

    def __init__(self):
        self._map_df = None
        self._map_fig = None
        self._output_loc = None
        self._value_column = None
        self._orientation = "odd-r"

    def load_map(self, hexmap, is_path=True, value_column=None, **kwargs):
        """
        Load the hex map
        :param hexmap: the filename of the map to load or the dataframe itself
        :param is_path: optional bool. If True, then hexmap is a path to the map csv.
                        Else it's a dataframe
        :param value_column: optional string. The name of the column in the csv
        """
        if is_path:
            hexmap = pd.read_csv(hexmap, **kwargs)
        cols = hexmap.columns
        for required_col in ("q", "r", "Constituency"):
            if required_col not in cols:
                raise RuntimeError(
                    "{} is not a column in the map dataframe. "
                    "Columns are {}.".format(required_col, cols)
                )
        self._map_df = hexmap

        if value_column is not None:
            self.value_column = value_column

    def add_data(self, data, map_join, data_join, is_path=True, **kwargs):
        """
        Add an extra dataframe to the hexmap dataframe.
        This can be used if the map dataframe contains the boundary information only,
        and you wish to add the variable which determines map colouring.
        :param data: Path to the additional dataframe, or the dataframe itself
        :param map_join: The column name in the map dataframe around which the data
                        should be joined
        :param data_join: The column name in the data dataframe around which the data
                        should be joined
        :param is_path: optional bool. If True, data is a path, else it's a dataframe
        """
        if self._map_df is None:
            raise RuntimeError("You should load a map first.")

        if is_path:
            data = pd.read_csv(data, **kwargs)

        self._map_df = (
            self._map_df.set_index(map_join)
            .join(data.set_index(data_join))
            .reset_index()
        )

    def draw_map(
        self,
        fig=None,
        _cmap="viridis",
        v_min=None,
        v_max=None,
        title=None,
        title_kwargs=None,
    ):
        """
        Create the map.
        :param fig: optional matplotlib fig object. If not provided, one is created.
        :param _cmap: optional string. Colormap to use in the plot. Default is viridis.
        :param v_min: optional float. The minimum value for the colormap.
                      If not provided, and a value column is, it's taken as
                      minimum value in the dataframe.
        :param v_max: optional float. The maximum value for the colormap.
                      If not provided, and a value column is, it's taken as
                      maximum value in the dataframe.
        :param title: optional string. Title to the figure
        :param title_kwargs: optional dict. Kwargs to the title
        :return: a matplotlib figure with the hex map drawn onto it.
        """
        if fig is None:
            fig, ax = plt.subplots(1, figsize=(8, 8))
            ax.axis("off")
        else:
            ax = fig.axes[0]

        y_min = 1000
        y_max = -1000

        # TODO allow other hex orientations. We assume odd-r here.
        d = 0.5 / np.sin(np.pi / 3)
        y_diff = np.sqrt(1 - 0.5 ** 2)
        patches = []
        colours = []
        for i in range(self._map_df.shape[0]):
            r = self._map_df.loc[i, "r"]
            q = self._map_df.loc[i, "q"]
            if self._value_column is not None:
                c = self._map_df.loc[i, self._value_column]
            else:
                c = 0.0

            if r % 2 == 1:
                # if in an odd row, we need to shift right
                q = q + 0.5
            r = y_diff * r
            hexagon = RegularPolygon((q, r), numVertices=6, radius=d, edgecolor="k")
            patches.append(hexagon)
            colours.append(c)

            # Get plot limits
            if r < y_min:
                y_min = r - 1.0
            if r > y_max:
                y_max = r + 1.0

        x_min = self._map_df["q"].min() - 1.0
        x_max = self._map_df["q"].max() + 1.0

        _cmap = _cmap if self._value_column is not None else None
        p = PatchCollection(patches, cmap=plt.get_cmap(_cmap), alpha=1.0)
        p.set_array(np.array(colours))

        if self._value_column is not None:
            # Set colorbar limits
            if v_min is None:
                v_min = self._map_df[self._value_column].min()
            if v_max is None:
                v_max = self._map_df[self._value_column].max()

            p.set_clim([v_min, v_max])
            plt.colorbar(p, shrink=0.5)

        ax.add_collection(p)

        ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])

        if title is not None:
            ax.set_title(title, fontdict=title_kwargs)

        self._map_fig = fig
        return fig

    def save_map(self, save_name, save_dir=None, **kwargs):
        """
        Save the figure
        :param save_name: the base name under which the map should be saved.
                          E.g. "myMap.png".
                          This is combined with the objects save_directory
                          to create a full save path.
        :param save_dir: optional string.
                         Directory in which to save the figure
        """
        if self._map_fig is None:
            raise RuntimeError(
                "You need to draw the map before attempting " "to save the figure."
            )

        # Update the object's save directory
        if save_dir is not None:
            self.save_directory = save_dir

        if self.save_directory is not None:
            save_name = os.path.join(self.save_directory, save_name)

        self._map_fig.savefig(save_name, **kwargs)

    def annotate_map(self, annotation, **kwargs):
        """
        Annotate the map
        :param annotation: The text to add to the figure
        :return: matplotlib figure of the map including the annotation
        """
        if self._map_fig is None:
            raise RuntimeError("Draw the map before adding an annotation to it.")

        ax = self._map_fig.axes[0]
        ax.annotate(annotation, **kwargs)

        return self._map_fig

    @property
    def value_column(self):
        return self._value_column

    @value_column.setter
    def value_column(self, _new_col):
        if self._map_df is None:
            raise RuntimeError("You should load a map before setting the value column.")

        if _new_col not in self._map_df.columns:
            raise KeyError(
                "Value column {} is not in the map dataframe. "
                "Columns are {}.".format(_new_col, self._map_df.columns)
            )
        else:
            self._value_column = _new_col

    @property
    def save_directory(self):
        return self._output_loc

    @save_directory.setter
    def save_directory(self, new_dir):
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        self._output_loc = new_dir

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, new_orientation):
        new_orientation = new_orientation.lower()
        if new_orientation == "odd-r":
            self._orientation = new_orientation
        elif new_orientation in ("even-r", "odd-l", "even-l"):
            raise NotImplementedError(
                "{} has not yet been implemented".format(new_orientation)
            )
        else:
            raise KeyError(
                "{} is not a recognised orientation.".format(new_orientation)
            )
