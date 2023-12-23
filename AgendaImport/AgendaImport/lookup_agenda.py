# This file allows the user to perform a lookup of the table that was created
# by import_agenda.py. This call assumes that the interview_test.db object
# was created and can be used accordingly for the function. 
# value is case sensitive but column is not, and we assume that the title
# will have an underscore in it. 
import sys
from db_table import db_table

# Error check user input 
if len(sys.argv) != 3:
    print('Usage: python lookup_agenda.py <column> <value>')
    print('Error: incorrect number of arguments')
    sys.exit(1)

# We assume that we already called import_agend.py, so
# we use it here accordingly. 
table = db_table('agenda', None)

column = sys.argv[1].lower()
value = '[' + sys.argv[2] + ']'
value = value.replace('\'', '\'\'')

column_name = ['date', 'time_start', 'time_end', 'session_title', 'description', 'room/location', 'speakers']
# check that column value is valid 
if not column in column_name:
    print('Usage: python lookup_agenda.py <column> <value>')
    print('Error: Failed to provide valid column name.')
    sys.exit(1)
column.replace(' ', '_')

# Initial lookup: Find all that match the original search
rand = dict()
rand.update({column : value})
initial_look = table.select(where=rand)
if column == 'speakers':
    # We need to do a special look for values that have a column like this value
    initial_look = table.selectIn(column, sys.argv[2])

final_list = []
# Look up all of the matching subssessions
for row in initial_look:
    final_list.append(row)
    # Search for the matching subssessions and append them to the final_list
    title = row.get('session_title').replace('\'', '\'\'')
    subsessions = table.selectIn('[session_or_\nsub-session(sub)]', title)
    if (len(subsessions) != 0):
        final_list.append(subsessions)
    
# Remove double '' and exterior brackets and print to console
for row in final_list:
    output = ""
    if isinstance(row, list):
        print(row)
    elif isinstance(row, dict):
        for col in column_name:
            output += str(row.get(col)) + "       "
        print(output + "\n")