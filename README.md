# Dropbox_API
This Python program connects to the Dropbox API with the intention of deleting files that are older than 90 days

It first makes a list of all files in your dropbox folder, then checks when the file was created. 
If the file is older than 90 days it then deletes it, and writes to a csv file the name, date of creation and date of deletion.
