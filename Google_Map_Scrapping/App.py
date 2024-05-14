import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
import os

def fetch_local_results(query, latitude, longitude):
    local_results = []
    i = 0
    while True:
        params = {
            "engine": "google_maps",
            "q": query,
            "ll": f"@{latitude},{longitude},21.1z",
            "type": "search",
            "api_key": "1c0d0d157cae2b4c6141913fbb2153e71107661901ea4cdb52dc0bc0be0ef196",
            "start": i
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        try:
            lcl_results = results["local_results"]
            local_results.extend(lcl_results)
            i += 1
        except (KeyError, IndexError):
            print(f"No local results found for page {i}.")
            break  # Exit the loop if no local results are found for the current page

    # Convert local_results to plain text
    plain_text = "\n".join(str(result) for result in local_results)
    return plain_text

def convert_to_excel(input_text, output_file_name):
    lines = input_text.split('\n')

    # Initialize a list to store all keys
    all_keys = set()

    # Parse each line and extract data
    for line in lines:
        try:
            result_dict = eval(line.strip())  # Convert string to dictionary
            all_keys.update(result_dict.keys())  # Add keys to the set
        except SyntaxError:
            print("Invalid line format:", line.strip())

    # Convert the set of keys to a list and sort them
    all_keys = sorted(list(all_keys))

    # Initialize a dictionary to store data for each key
    data = {key: [] for key in all_keys}

    # Parse each line again and extract data for each key
    for line in lines:
        try:
            result_dict = eval(line.strip())  # Convert string to dictionary
            for key in all_keys:
                data[key].append(result_dict.get(key, ""))  # Append data for each key
        except SyntaxError:
            print("Invalid line format:", line.strip())

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Get the directory of the input file
    output_dir = os.getcwd()  # Current working directory
    output_file_path = os.path.join(output_dir, output_file_name)

    # Save DataFrame to Excel file
    df.to_excel(output_file_path, index=False)

    return output_file_path

# Streamlit app
def main():
    st.title("Google Maps Data Scrapping")

    # Input fields
    query = st.text_input("Type required search(like,hotels,schools,malls,etc: ")
    latitude = st.text_input("Enter latitude: ")
    longitude = st.text_input("Enter longitude: ")

    if st.button("Fetch Local Results"):
        if query and latitude and longitude:
            with st.spinner("Fetching local results..."):
                plain_text = fetch_local_results(query, latitude, longitude)
            st.success("Local results fetched successfully.")
            
            # Convert plain text to Excel
            with st.spinner("Converting to Excel..."):
                output_file_path = convert_to_excel(plain_text, "output_excel_file.xlsx")
            st.success("Conversion completed successfully.")

            # Provide a link to download the Excel file
            st.markdown(
                f"[Download Excel file]({output_file_path})",
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()
