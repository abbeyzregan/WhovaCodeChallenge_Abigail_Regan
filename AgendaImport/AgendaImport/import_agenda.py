# This python script takes the given .xls file and writes it into the
# database using the db_table.py function. 
# The .xls file mentioned must be in the same directory as the call 
# to import_agenda.py

# Constraints from db_table.py still apply here. If the user wishes
# to perform a schema update, it is up to them to manually 
# remove interview_test.db from their computer. 
import sys
from db_table import db_table
import pandas as pd
import math

# Check that input is valid
if len(sys.argv) != 2:
    print('Usage: python import_agenda.py <valid.xls file>')
    sys.exit(1)

# Get file name and try to read in file
file = pd.read_excel(sys.argv[1], skiprows=14)

columns = dict()
for col in file.columns:
    # I chose to add brackets so users can have their SQL column
    # names in any format that they choose. I also assume that
    # users do not need to include '*' characters that they are
    # provided in the sample code but not used for lookups
    col = '[' + col.replace('*', '').replace(' ', '_') + ']'
    col = col.lower()
    columns.update({col : 'text'})
# Extract info needed to use db_table.py
table = db_table('agenda', columns)

# Iterate through the rows of database and update the table
last_title = ""
for index, row in file.iterrows():
    # Get a map of the header value to the 
    row_dict = dict()
    for col in file.columns:
        val = row[col]
        col = col.lower()
        if not (isinstance(val, float) and math.isnan(val)):
            col = '[' + col.replace('*', '').replace(' ', '_') + ']'
            if isinstance(val, str):
                val = '[' + val + ']'
                val = val.replace('\'', '\'\'')
            row_dict.update({col: val})
    if '[Session]' == row_dict.get("[Session_or_\nSub-session(Sub)]"):
        last_title = row_dict.get("[Session_or_\nSub-session(Sub)]")
    else:
        val = "Subsession of " + last_title 
        row_dict.update({"[Session_or_\nSub-session(Sub)]": val})
    table.insert(row_dict)

# We are done for now, close the database connection
table.close()