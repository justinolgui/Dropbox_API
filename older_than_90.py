# Import all the necessary Python Modules
import requests
import json
import dropbox
import datetime
import pandas as pd
import pytz
from pytz import timezone

# Connect to our Dropbox account
dbx = dropbox.Dropbox('Your Secret Access Token')

# Create an empty list to store our file names
files_folders = []
# List all files in the account, use recursive to get files in subfolders
for entry in dbx.files_list_folder('', recursive=True).entries:
    files_folders.append(entry.path_display)

# Create an empty list that we will fill with files older than 90 days
files_to_del = []

# Create a function to check date of files
def greater_than_90(files): 
    # loop through all files in dropbox folder
    for file in files:
        '''
        In dropbox, folders do not have a server_modified timestamp method. 
        So when we try to call this method it will throw an attribute error.
        As a result we use the try, except block to pass over folders
        '''
        try:
            # create a variable that will store our file path
            f_path = file
            
            # create a variable that will store our file creation date
            file_creation_date = dbx.files_get_metadata(file).server_modified.date()
            file_creation_datetime = dbx.files_get_metadata(file).server_modified            
            
            # create a variable that will store today's date
            today = datetime.date.today()
            
            # create a variable that will store the length of time the file has existed
            time_passed = (today - file_creation_date).days
            
            # check if this file is older than 90 days
            if time_passed < 90:
                # add file path to our list of files to delete
                files_to_del.append(f_path)        
            
        except AttributeError:
            pass
    
    # Check to see if our files to delete list is empty
    if not files_to_del:
        print("\nThere are no files older than 90 days! \n")
    else:
        # Call our delete files function with our files to delete list if it's not empty
        delete_files(files_to_del)
        
    

# Create two empty lists to capture our file name and the date_time of deletion
del_file_name = []
del_file_date = []
file_creation_timestamp = []

# Create a function to delete files
def delete_files(files_to_delete):
    # Loop through all files in our files to delete list
    for file in files_to_delete:
        # Create a variable to store the metadata of our file deletion
        del_file = dbx.files_delete(file)
        
        # Add the name of the file to our deleted file name list
        del_file_name.append(del_file.name)      
        
        # Add the date and time that the file was created
        file_creation_timestamp.append(del_file.server_modified)

        # Add the time we deleted the file
        del_file_date = datetime.datetime.utcnow()
        
    # Create a DataFrame that stores the file name and deleted date
        df = pd.DataFrame(
            {'Deleted File Name': del_file_name,             
             'Date_Time of File Creation': file_creation_timestamp,
             'Date_Time of Deletion': del_file_date
            })

    # Write our stored data to a Pandas DataFrame
    df.to_csv('Deleted_Dropbox_Files.csv', index=False)

    # Let the user know files were deleted
    print("\nA csv file with deleted file data has been created\n") 

# Call our greater_than_90 function
greater_than_90(files_folders)