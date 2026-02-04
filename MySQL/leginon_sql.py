#!/usr/bin/env python

import os
import MySQLdb
import ConfigParser
import optparse
import csv
from collections import defaultdict

# Setup parser for our configuration file:
parse = ConfigParser.SafeConfigParser()
# Parse the configuration file:
parse.read('/etc/myami/sinedon.cfg')

parser = optparse.OptionParser()
parser.add_option("--scope", dest="scope", help="Path scope to restrict reports to.")

options, args = parser.parse_args()

# Connect to Leginon database:

def retrieve_all_projects():

    """
    Return all the projects in the database.

    The returned object is a dictionary of tuples, where the key is the project_id and the value is a tuple
    containing the name, short_description, and long_description.
    """

    # Open database connection
    db = MySQLdb.connect(host=parse.get('global', 'host'), user=parse.get('global', 'user'), passwd=parse.get('global', 'passwd'), db=parse.get('projectdata', 'db'))
    # Prepare a cursor object using the cursor() method
    cursor = db.cursor()
    # Temporary defaultdict with lists as values, which will be converted to tuples. This way you are appending to
    # lists and not recreating tuples.
    d1 = defaultdict(list)

    try:
        # Execute the SQL command to get all projects
        cursor.execute("SELECT DEF_id, name, short_description, long_description FROM projects")
        # Fetch all the rows in a tuple of tuples.
        results = cursor.fetchall()
        for row in results:
            d1[row[0]].append(row[1])
            d1[row[0]].append(row[2])
            d1[row[0]].append(row[3])
    except:
        raise Exception('Unable to fetch data from the projects table.')
    finally:
        # Disconnect from database
        db.close()
    # Convert the temporary defaultdict that contains lists as values to tuples.
    projects = dict((k, tuple(v)) for k, v in d1.iteritems())
    cursor.close()
    # projects is a dictionary of tuples.
    # projects = {project_id: (name, short_description, long_description), }
    return projects

def main():
    # {project_id: (name, short_description, long_description),}
    projects = retrieve_all_projects()
#   project_owners = retrieve_all_projectowners()
#   project_experiments = retrieve_all_projectexperiments()
#   users = retrieve_all_users()
#   sessions = retrieve_all_sessions()

    for k, v in projects.iteritems():
        print "\nProject Name: {}".format(v[0])
#       print "    Project Owned by: "
        # If the project has any owners associated with it.
#       if k in project_owners:
#           for x in project_owners[k]:
#               try:
#                   print "        {}".format(users[x][0])
#               except KeyError:
#                   pass
#       else:
#           print "        None"
        print "    Project Sessions:"

if __name__ == '__main__':
    main()
