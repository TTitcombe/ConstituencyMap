import os

import altair as alt
import numpy as np
import pandas as pd


class AltairMap:
    """
    AltairMap creates an interactive map with altair.
    """
    def __init__(self):
        self._map_df = None
        self._value_column = None
        self._orientation = "odd-r"
        self._colour_map = {"Conservative": "darkblue",
                            "Labour": "red",
                            "Lib Dem": "orange",
                            "Green": "green",
                            "Scottish National Party": "yellow",
                            "Plaid Cymru": "black",
                            "Sinn Fein": "darkgreen",
                            "Speaker": "lightgray"}

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
                raise RuntimeError("{} is not a column in the map dataframe. "
                                   "Columns are {}.".format(required_col, cols))
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

        self._map_df = self._map_df.set_index(map_join).join(data.set_index(data_join)).reset_index()

    def draw_map(self):
        domain, range_ = self._get_colour_scaling()
        colours_obj = alt.Color("Party:N",
                                scale=alt.Scale(
                                    domain=domain,
                                    range=range_),
                                legend=None)

        chart = alt.Chart(self._map_df).mark_circle().encode(
            x='q',
            y='r',
            color=colours_obj,
            size=alt.value(50),
            tooltip=['Constituency:N'],
        ).interactive()

        legend = alt.Chart(self._map_df).mark_circle().encode(
            y=alt.Y('Party:N', axis=alt.Axis(orient='right')),
            color=colours_obj,
        )

        return chart | legend

    def _get_colour_scaling(self):
        domain = list(self._colour_map.keys())
        range_ = list(self._colour_map.values())

        for party in self._map_df["Party"].unique():
            if party not in domain:
                domain.append(party)
                range_.append("black")

        return domain, range_
