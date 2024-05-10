import streamlit as st
import pandas as pd
import re
import os
from io import BytesIO

st.title("Distress Data Quality Checks")
st.text("This app is used to checks errors from excel file")
# Define your pattern
pattern = r'\.{2,}|[*]{2,}'

# File upload
excel_file = st.file_uploader("Upload Excel file:", type="xlsx")

# Output file path input
output_path = st.text_input("Enter output file path:", value="qc.xlsx")

# Button to start quality checks
if st.button("Start Quality Checks"):
    # Check if file is uploaded
    if excel_file is not None:
        # Read the Excel file into a DataFrame
        with BytesIO(excel_file.getvalue()) as buffer:
            df = pd.read_excel(buffer, sheet_name="Sheet1")

        # Initialize a list to store responses
        dic = []

        # Iterate over the rows of the DataFrame
        for index, row in df.iterrows():
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
        st.info("Please upload an Excel file.")
