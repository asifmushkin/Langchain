import streamlit as st
import pandas as pd
from serpapi import GoogleSearch

def fetch_local_results(query, latitude, longitude, out_file_name):
    local_results = []
    i = 0
    while True:
        params = {
            "engine": "google_maps",
            "q": query,
            "ll": f"@{latitude},{longitude},21.1z",
            "type": "search",
            "api_key": "ef953cf9cb5bee9b78f26bc0e1a229fef9cb8b4d57849371857e0acab647c540",
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

    # Save local_results to a file
    with open(out_file_name, 'w') as file:
        for result in local_results:
            file.write(str(result) + '\n')

    return out_file_name

def convert_to_excel(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

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

    # Save DataFrame to Excel file
    df.to_excel(output_file_path, index=False)

# Streamlit app
def main():
    st.title("Local Results to Excel Converter")

    # Input fields
    query = st.text_input("Type required search")
    latitude = st.text_input("Enter latitude")
    longitude = st.text_input("Enter longitude")
    out_file_name = st.text_input("Enter output file name")

    if st.button("Fetch Local Results"):
        if query and latitude and longitude and out_file_name:
            with st.spinner("Fetching local results..."):
                file_path = fetch_local_results(query, latitude, longitude, out_file_name)
            st.success(f"Local results fetched successfully. Saved to {file_path}")

    # File uploader
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

    if uploaded_file is not None:
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type}
        st.write(file_details)

        # Convert text to Excel
        if st.button("Convert to Excel"):
            with st.spinner("Converting..."):
                convert_to_excel(uploaded_file.name, "output_excel_file.xlsx")
            st.success("Conversion completed successfully. Download your Excel file below.")

            # Download link for the converted Excel file
            st.markdown("[Download Excel file](output_excel_file.xlsx)", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
