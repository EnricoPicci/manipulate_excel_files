import pandas as pd
import os
import datetime


def get_excel_file_paths(folder_path):
    # read all the paths of all the excel files in the folder and in all subfolders recurvisely
    excel_files = [
        os.path.join(root, file)
        for root, dirs, files in os.walk(folder_path)
        for file in files
        if file.endswith(".xlsx")
    ]
    return excel_files


# read excel files is a function that reads a list of paths to excel files and returns a list of dictionaries
# each dictionary contains the data from the excel file and the date of the last modification of the file
def read_excel_files(excel_files, mandatory_columns=[]):
    list_of_dicts = []
    for file in excel_files:
        # Read the Excel file
        df = pd.read_excel(file)

        # check that the file contains the mandatory columns
        for column in mandatory_columns:
            assert column in df.columns

        # Get the modification time of the file
        mod_time = os.path.getmtime(file)
        date = datetime.datetime.fromtimestamp(mod_time)

        # Add the date to the DataFrame
        df["date"] = date
        # Add the file path to the DataFrame
        df["file_path"] = file

        # Convert the DataFrame to a list of dictionaries
        list_of_dicts.extend(df.to_dict("records"))
    return list_of_dicts


def records_from_excel_files(folder_path, mandatory_columns=[]):
    excel_files = get_excel_file_paths(folder_path)
    return read_excel_files(excel_files, mandatory_columns)
