# Avenue for no matches found

# Make arguments for different inputs
    # Make default of time input the most recent run

# Can filter by date, project, etc. 
    # Then grab list of all id/name of runs that match criteria (can export filtered data to file, maybe dataframe?)
    # Then use that to grab sample sheet (for loop?)

# Example of basespace CLI code to get information I need
# The --project-name option is WAY faster than using the --filter-field option
# $ bs list datasets -F Project.Name -F AppSession.Name -F AppSession.DateCompleted --project-name={project name} --filter-field={a dataset header} --filter-term={to look for in field}

# Example of basespace CLI code to get info based on date
# Only know for sure d/y works for time. Need to check for h/m/s
# Default for date filter is DateModified -> set --date-field option to DateCompleted
# $ bs list datasets -F Project.Name -F Appsession.Name -F AppSession.DateCompleted --date-field=DateCompleted --newer-than={time (d/y)} / --older-than={time}

#  --no-metadata stops json file from being created
# $ bin/bs download project -n Practice -o ~/micromamba/envs/sample_sheets --exclude '*' --include '*SampleSheet.csv' --no-metadata 

# Extract SampleSheet.csv files from undefined number of directories and move to current directory
# Each instance overwrites itself. Could leave out -exec option and perform task(s) on each SampleSheet before moving onto next
# Just use file paths given by find and have commands/functions reach into directories to get file
# $ find ./ -type f -name 'SampleSheet.csv' -exec mv {} ./ \;

# Can grab files based on text in file
# $ find /home/sara/Documents -type f -exec grep -l "example" {} +
# subprocess.check_output(['ls', '-l'])

# Project given -> pulls dataset list and whatever other list will match with other data given/needed (i.e. run name)
# Can only connect run name and project based on DateCreated columns

#!/bin/python3
import os
def fromProject(project_name: str, output_location: str, most_recent=False, **kwargs):
    if not isinstnace(kwargs.get('run_names'), list):
        raise TypeError('run_names must be a list')
    run_names = kwargs.get('run_names')
    newer_than = kwargs.get('newer_than')
    older_than = kwargs.get('older_than')
    optional_params = [run_names, newer_than, older_than]
    if all(i == optional_params[0] for i in optional_params) is True:
        # grab SampleSheet.csv based on project_name and output_location only

class Run:
    
    # Instance attributes
    self.run_name = run_name
    self.project_name = project_name
    self.date_completed = date_completed

    # Grab sample sheets of run from certain project
    # Make run_name, newer_than, and older_than optional (if they are not already)
    # Will have to get run names for each project
        # Could overlap tables?
    def fromProject(self, project_name, output_location, run_name:list, newer_than="", older_than=""):
        self.project_name = project_name
        # $ bs download project -n <project name> -o <output> --extension csv
        self.output_location = output_location
Run()