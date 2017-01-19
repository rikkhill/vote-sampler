# Take postcode and election data, strip extraneous details, and dump them into CSV files

import pandas as pd

# `Candidates` sheet from general election results
candidates = pd.read_excel("./data/2015-UK-general-election-data-results-WEB.xlsx", sheetname="Candidates")
candidates = candidates[["Constituency ID ", "Party abbreviation", "Votes"]]
candidates.columns = ["constituency_id", "party", "votes"]
candidates.to_csv("./data/candidates.csv", index=False)

# `Constituency` sheet from general election results
constituency = pd.read_excel("./data/2015-UK-general-election-data-results-WEB.xlsx", sheetname="Constituency")
constituency["Valid Turnout"] = constituency["Valid Votes"] / constituency["Electorate"]
constituency = constituency[["Constituency ID", "Constituency Name", "Valid Turnout"]]
constituency.columns = ["constituency_id", "constituency_name", "valid_turnout"]
constituency.to_csv("./data/constituency.csv", index=False)

# Postcode lookup, augmented with turnout
postcodes = pd.read_csv("./data/2015.04.03.postcode_to_constituency_lookup.tsv", encoding="ISO-8859-1", sep="\t", header=None)
postcodes.columns = ["postcode", "constituency_id", "constituency_name"]

# Include turnout in postcodes for sampling purposes
postcodes = pd.merge(postcodes, constituency, on="constituency_id")
postcodes = postcodes[["postcode", "constituency_id", "valid_turnout"]]
# Remove spaces from postcode
postcodes["postcode"] = postcodes['postcode'].replace(regex=True, to_replace=r' ', value=r'')
postcodes.to_csv("./data/postcodes.csv", index=False)
