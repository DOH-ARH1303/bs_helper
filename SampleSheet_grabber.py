
# Avenue for no matches found

# Make arguments for different inputs
    # Make default of time input the most recent run

# Can filter by date, project, etc. 
    # Then grab list of all id/name of runs that match criteria (can export filtered data to file, maybe dataframe?)
    # Then use that to grab sample sheet (for loop?)

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
# $ bin/bs download project -n Practice -o ~/micromamba/envs/sample_sheets --exclude '*' --include '*SampleSheet.csv' --no-metadata | find ./ -type f -name 'SampleSheet.csv'

# Extract SampleSheet.csv files from undefined number of directories and move to current directory
# Each instance overwrites itself. Could leave out -exec option and perform task(s) on each SampleSheet before moving onto next
# Just use file paths given by find and have commands/functions reach into directories to get file
# $ find ./ -type f -name 'SampleSheet.csv' -exec mv {} ./ \;

# Not usually worth grabbing by project and run_name. If they have run_name, can grab sample sheet and then parse by project and vice versa
# Still relevant to grab based on list of samples/biosamples

# Can grab files based on text in file
# $find /home/sara/Documents -type f -exec grep -l "example" {} +

#!/bin/python3
import subprocess

class SampleSheetGrabber():
    def __init__(self, api_server, access_token, entity, output_location):
        self.api_server = api_server
        self.access_token = access_token
        self.entity = entity
        self.base_command = f"bs --api-server={api_server} --access-token={access_token} download {entity}"
        # This might get standardized
        self.output_location = output_location
        # SampleSheets get download in a series of directories. This lists the directory paths
        self.find_command = "find ./ -type f -name 'SampleSheet.csv'"


        # Alternatively, add self.entity to each function for potential entities and set default value to False
        @property
        def entity(self):
            return self._entity
        
        @entity.setter
        def entity(self, new_entity):
            valid_entities = ["project", "run", "biosamples", "dataset"]
            if new_entity not in valid_entities:
                raise ValueError(f"Value must be one of: {valid_entities}")
            self._entity = new_entity


    def set_project_name(self, project_name):
        self.project_name = project_name
    
    def set_run_name(self, run_name):
        self.run_name = run_name

    def set_most_recent(self, most_recent):
        self.most_recent = most_recent

    def set_newer_than(self, newer_than):
        self.newer_than = newer_than

    def set_older_than(self, older_than):
        self.older_than = older_than

    def set_biosamples(self, biosamples):
        self.biosamples = biosamples

    def build_command(self):
        command = [self.base_command]

        if hasattr(self, 'project_name'):
            command.append(f" -n {self.project_name}")
        


# PROCEDURAL STRUCTURE
# api_server = ""
# access_token = ""
# bs_command = f"bs --api-server={api_server} --access-token={access_token}"
# find_samplesheet_command = "find ./ -type f -name 'SampleSheet.csv'"

# def fromProject(project_name: str, output_location: str, most_recent=False, **kwargs):
#     if not isinstnace(kwargs.get('run_names'), list):
#         raise TypeError('run_names must be a list')
#     run_names = kwargs.get('run_names')
#     newer_than = kwargs.get('newer_than')
#     older_than = kwargs.get('older_than')
#     biosamples = kwargs.get('biosamples')
#     optional_params = [run_names, newer_than, older_than]
#     if all(i == optional_params[0] for i in optional_params) is True:
#         # grab SampleSheet.csv based on project_name and output_location only
#         subprocess.run(f"{bs_command} download project -n {project_name} -o {output_location} --exclude '*' --include '*SampleSheet.csv' --no-metadata", shell=True)
#         samplesheet_paths = subprocess.run(f"{find_samplesheet_command}", shell=True)