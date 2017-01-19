# Create an artificial constituency from the outward part of postcodes
# For example, the W12 postcode area, or the BA1 postcode area

import pandas as pd
import sys

filename = sys.argv[1]
args = sys.argv[2:]

# Get a list of postcodes
postcodes = pd.read_csv("./data/postcodes.csv")
postcodes = postcodes["postcode"]

# Filter by outward postcode
filtered_postcodes = []

for outward_code in args:
    filtered_postcodes += postcodes[postcodes.str.contains("^" + outward_code + "...", case=False)].tolist()

with open(filename, "w") as f:
    for code in filtered_postcodes:
        f.write("%s\n" % code)

