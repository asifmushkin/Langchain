import streamlit as st
import pandas as pd
import re
import os
from io import BytesIO
import pyodbc
breakpoint
st.title("Distress Data Quality Checks")
st.text("This app is used to checks errors from mdb files")

def read_mdb(x):
    mdb_files = []
    for root, dirs, files in os.walk(x):
        for file in files:
            if file.endswith(".mdb"):
                mdb_files.append(os.path.join(root, file))
    return mdb_files

#defining function to read tables in mdb
def read_tables_by_prefix(mdb_file, table_prefix):
    conn_str = f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};Dbq={mdb_file};"
    connection = pyodbc.connect(conn_str)
    cursor = connection.cursor()

    tables = []
    for table_info in cursor.tables(tableType='TABLE'):
        table_name = table_info.table_name
        if table_name.startswith(table_prefix):
            tables.append(table_name)

    data = pd.DataFrame()
    for table in tables:
        query = f"SELECT * FROM [{table}]"
        table_data = pd.read_sql(query, connection)
        table_data['Survey_ID_1'] = os.path.splitext(os.path.basename(mdb_file))[0]
        data = pd.concat([data, table_data], ignore_index=True)

    connection.close()
    return data

# File upload
mdb_directory = st.file_uploader("Enter the directory containing MDB files:", type="")

# Output file path input
output_path = st.text_input("Enter output file path:", value="qc.xlsx")

# Button to start quality checks
if st.button("Start Quality Checks"):
    # Check if directory is uploaded
    if mdb_directory is not None:
        # Read MDB files
        mdb_files = read_mdb(mdb_directory)
        
        # Dataframe to store merged data
        DV_keycode = pd.DataFrame()

        # Extract and merge data from MDB files
        for mdb_file in mdb_files:
            dt_vedio = read_tables_by_prefix(mdb_file, "dt_VideoKeyCode_Raw")
            DV_keycode = pd.concat([DV_keycode, dt_vedio], ignore_index=True)

        # Filtering dataframe to remove calibration rows
        DV_keycode_filtered = DV_keycode[~DV_keycode['SURVEY_ID'].str.startswith('CALIBRATION')]
        DV_keycode_filtered.to_excel(output_path, index=False)

        st.success(f"Data extracted and saved to {output_path}")
        
        # Perform quality checks
        # Define your pattern
        pattern = r'\.{2,}|[*]{2,}'

        # Initialize a list to store responses
        dic = []

        # Iterate over the rows of the DataFrame
        for index, row in DV_keycode_filtered.iterrows():
            quantity = str(row["COMMENT_1"])  # Ensure quantity is treated as a string
            object_id = row["OBJECTID"]
            event_desc = row["EVENT_DESC"]
            severity = row["COMMENT"]
            chainage_start = row["CHAINAGE_START"]
            chainage_end = row["CHAINAGE_END"]
            distress_length = row["LENGTH"]
            frame_start = row["FRAME_START"]
            frame_end = row["FRAME_END"]
            pav_remarks = row["COMMENT_2"]

            # Perform your checks as before, using DataFrame values
            matches = re.findall(pattern, quantity)
            if matches:
                response = f"Check for quantity: {quantity}"
                dic.append(response)
            elif chainage_start == chainage_end and distress_length != 0:
                response = f"Difference between chainage & distress length found: Length: {distress_length}, Chainage start: {chainage_start}, Chainage end: {chainage_end}"
                dic.append(response)
            # Add other checks here

        # Create a DataFrame from the list of responses
        df_response = pd.DataFrame(dic, columns=["Remarks"])

        # Export the DataFrame to an Excel file
        df_response.to_excel(output_path, index=True, index_label="ser#")
        
        st.success(f"Found {len(dic)} errors! Successfully saved quality checks as Excel file.")
        st.write(f"You can download the file from [this link]({output_path}).")
    else:
        st.info("Please upload a directory containing MDB files.")
