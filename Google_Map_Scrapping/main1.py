import streamlit as st
from serpapi import GoogleSearch
import pandas as pd

def main():
    st.title("Google Maps Search")

    # Input fields
    query = st.text_input("Type required search:", "universities")
    latitude = st.text_input("Enter latitude:", "")
    longitude = st.text_input("Enter longitude:", "")
    out_file_name = st.text_input("Enter output file name:", "output")

    # Button to trigger search
    if st.button("Search"):
        # Perform search
        params = {
            "engine": "google_maps",
            "q": query,
            "ll": f"@{latitude},{longitude},21.1z",
            "type": "search",
            "api_key": "9b80245c3ff61daa0b14f66b63958c375aecfd171e9deba93811e90b50667dfd"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        local_results = results["local_results"]

        dfs = []
        for x in range(len(local_results)):
            result = local_results[x]
            df = pd.DataFrame.from_dict(result, orient='index')
            df = df.transpose()
            dfs.append(df)

        final_df = pd.concat(dfs, ignore_index=True)

        # Write DataFrame to Excel file
        file_path = f"Data/{out_file_name}.xlsx"
        final_df.to_excel(file_path, index=True)

        # Show the first 10 rows
        st.write(final_df.head(10))

        # Provide download link for the Excel file
        st.markdown(get_download_link(file_path), unsafe_allow_html=True)

def get_download_link(file_path):
    """Generates a link allowing the file to be downloaded."""
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/xlsx;base64,{b64}" download="output.xlsx">Download Excel File</a>'
    return href

if __name__ == "__main__":
    main()
