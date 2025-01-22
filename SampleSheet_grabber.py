# Avenue for no matches found

# Example of basespace CLI code to get information I need
# The --project-name option is WAY faster than using the --filter-field option
# $ bs list datasets -F Project.Name -F AppSession.Name -F AppSession.DateCompleted --project-name={project name} --filter-field={a dataset header} --filter-term={to look for in field}

# Example of basespace CLI code to get info based on date
# Only know for sure d/y works for time. Need to check for h/m/s
# Default for date filter is DateModified -> set --date-field option to DateCompleted
# $ bs list datasets -F Project.Name -F Appsession.Name -F AppSession.DateCompleted --date-field=DateCompleted --newer-than={time (d/y)} / --older-than={time}

#  --no-metadata stops json file from being created
# $ bin/bs download project -n Practice -o ~/micromamba/envs/sample_sheets --exclude '*' --include '*SampleSheet.csv' --no-metadata | find ./ -type f -name 'SampleSheet.csv'

# Extract SampleSheet.csv files from undefined number of directories and move to current directory. Hyphinate w/ run name?
# Each instance overwrites itself. Could leave out -exec option and perform task(s) on each SampleSheet before moving onto next
# Just use file paths given by find and have commands/functions reach into directories to get file
# $ find ./ -type f -name 'SampleSheet.csv' -exec mv {} ./ \;

# Not usually worth grabbing by project and run_name. If they have run_name, can grab sample sheet and then parse by project and vice versa
# Still relevant to grab based on list of samples/biosamples

# Can grab files based on text in file
# $find /home/sara/Documents -type f -exec grep -l "example" {} +

#!/bin/python3
import subprocess

class SampleSheetGrabber:
    def __init__(self, api_server, access_token, output_location):
        self.api_server = api_server
        self.access_token = access_token
        self.base_command = f"bs --api-server={api_server} --access-token={access_token}"
        self.download_flags = "--exclude '*' --include '*SampleSheet.csv' --nometadata"
        # This might get standardized
        self.output_location = output_location
        # SampleSheets get download in a series of directories. This lists the directory paths
        self.find_command = "find ./ -type f -name 'SampleSheet.csv'"

class OptionalAttributes:
    # Either class or the other attributes
    def __init__(self): 
        self.project_name = None 
        self.most_recent = None 
        self.newer_than = None 
        self.older_than = None 
        self.biosamples = None 
        self.run_name = None

    def set_project_name(self, project_name):
        self.project_name = project_name
    def set_most_recent(self, most_recent_run):
        self.most_recent_run = most_recent_run
    def set_newer_than(self, newer_than):
        self.newer_than = newer_than
    def set_older_than(self, older_than):
        self.older_than = older_than
    def set_biosamples(self, biosamples):
        self.biosamples = biosamples
    def set_run_name(self, run_name):
        self.run_name = run_name

class Project:
    def __init__(self, project_name, api_server, access_token, output_location):
        self.project_name = project_name
        self.sample_sheet_grabber = SampleSheetGrabber(api_server, access_token, project_name, output_location)
        self.optional_attr = OptionalAttributes()
    def build_command(self):
        command = [self.sample_sheet_grabber.base_command, 'download project', f'-o {self.sample_sheet_grabber.output_location}']
        # -n {self.project_name} might need to add back here. Might be better to add at the end?
        list_command = f'{self.sample_sheet_grabber.base_command} list projects'
        # # Would make more sense as a separate class or function. Project name = required attribute
        # if hasattr(self.optional_attr.most_recent_run):    
        #     sorted_projects = subprocess.run(f'{self.sample_sheet_grabber.base_command} list projects --sort-by=DateCreated', shell=True, capture_output=True, text=True)
        #     # might need an extra step to make sorted_projects a list of dictionaries
        #     most_recent_project_name = sorted_projects[0].get("Name")
        #     list_command.append(f'-n {most_recent_project_name}')

        if hasattr(self.optional_attr.newer_than):
            sorted_projects = subprocess.run(f'{self.sample_sheet_grabber.base_command} list projects --newer-than={self.optional_attr.newer_than}', shell=True, capture_output=True, text=True)
            command.append(f'--date-field=DateCreated ')
        return " ".join(command)
class Run:
    def __init__(self, run_name):
        self.run_name = run_name
        self.sample_sheet_grabber = SampleSheetGrabber()
        self.optional_attr = OptionalAttributes()

class Biosamples:
    def __init__(self, biosamples):
        self.biosamples = biosamples
        self.sample_sheet_grabber = SampleSheetGrabber()
        self.optional_attr = OptionalAttributes()

class Dataset:
    def __init__(self, project_name, biosamples):
        self.project_name = project_name
        # Will have to account for L001/L1
        self.biosamples = biosamples
        self.sample_sheet_grabber = SampleSheetGrabber()    
        self.optional_attr = OptionalAttributes()
   
    def build_command(self):
        command = [self.base_command]


# Useful for determining if optional attributes have values and what to do with them (i.e. parse sample sheets for run names/biosamples)
        # if self.entity == 'project':
        #     def project(self, project_name):
        #         if not hasattr(self, 'project_name') or getattr(self, 'project_name') is None:
        #             raise ValueError(f"project_name is required for project entity")
        #         command.append(f" -n {self.project_name}")
        
        


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