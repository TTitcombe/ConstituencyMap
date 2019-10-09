import csv
import json
import os

hexjson_file = os.path.join("data", "boundaries", "uk_hex.hexjson")
with open(hexjson_file, "r", encoding="utf8") as json_file:
    hex = json.load(json_file)["hexes"]
data = []
for _, values in hex.items():
    data.append(
        {
            "Constituency": values["n"],
            "q": values["q"],
            "r": values["r"],
            "Electorate": values["e"],
            "Population": values["p"],
        }
    )

keys = data[0].keys()
save_name = os.path.join("data", "boundaries", "uk_hex.csv")
with open(save_name, "w") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)
