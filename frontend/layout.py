import streamlit as st
from pathlib import Path
import shutil

# Import all backend conversion functions
from backend.csv_to_json import csv_to_json
from backend.csv_to_parquet import csv_to_parquet
from backend.csv_to_xlsx import csv_to_xlsx
from backend.json_to_csv import json_to_csv
from backend.json_to_parquet import json_to_parquet
from backend.json_to_xlsx import json_to_xlsx
from backend.parquet_to_csv import parquet_to_csv
from backend.parquet_to_json import parquet_to_json
from backend.parquet_to_xlsx import parquet_to_xlsx
from backend.xlsx_to_csv import xlsx_to_csv
from backend.xlsx_to_json import xlsx_to_json
from backend.xlsx_to_parquet import xlsx_to_parquet

# Define the folder to save uploaded files
UPLOAD_FOLDER = Path("data")
UPLOAD_FOLDER.mkdir(exist_ok=True)

def cleanup_file(file_path):
    """Remove the specified file if it exists."""
    if file_path.exists():
        file_path.unlink()

def convert_file(file_path, file_type, target_format):
    """Perform the file conversion based on the selected formats."""
    conversion_functions = {
        ("csv", "JSON"): csv_to_json,
        ("csv", "Excel (XLSX)"): csv_to_xlsx,
        ("csv", "Parquet"): csv_to_parquet,
        ("json", "CSV"): json_to_csv,
        ("json", "Excel (XLSX)"): json_to_xlsx,
        ("json", "Parquet"): json_to_parquet,
        ("xlsx", "CSV"): xlsx_to_csv,
        ("xlsx", "JSON"): xlsx_to_json,
        ("xlsx", "Parquet"): xlsx_to_parquet,
        ("parquet", "CSV"): parquet_to_csv,
        ("parquet", "JSON"): parquet_to_json,
        ("parquet", "Excel (XLSX)"): parquet_to_xlsx,
    }
    output_file = file_path.with_suffix(f".{target_format.lower().replace('excel (xlsx)', 'xlsx')}")
    conversion_function = conversion_functions.get((file_type, target_format))
    if conversion_function:
        conversion_function(file_path, output_file)
    return output_file

def app_layout():
    # Page configuration
    st.set_page_config(page_title="File Conversion App", page_icon="🔄", layout="wide")

    # Sidebar navigation
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Conversion History"])

    if page == "Home":
        render_home()
    elif page == "Conversion History":
        render_history()

def render_home():
    st.title("🌟 File Conversion App 🌟")
    st.markdown("""
        Welcome to the **File Conversion App**! Convert files between CSV, JSON, XLSX, and Parquet seamlessly. 
        Upload your files, choose the format, and download the converted files. 🚀
    """)

    uploaded_files = st.file_uploader(
        "Upload files for conversion:", 
        type=["csv", "json", "xlsx", "parquet"], 
        accept_multiple_files=True, 
        help="You can upload multiple files."
    )

    if uploaded_files:
        conversion_history = st.session_state.get("conversion_history", [])
        for uploaded_file in uploaded_files:
            st.write(f"**Uploaded File:** `{uploaded_file.name}`")
            file_path = UPLOAD_FOLDER / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            file_type = uploaded_file.name.split(".")[-1].lower()
            target_format = st.selectbox(
                f"Select target format for `{uploaded_file.name}`:",
                options=["JSON", "Excel (XLSX)", "Parquet"] if file_type == "csv" else 
                        ["CSV", "Excel (XLSX)", "Parquet"] if file_type == "json" else 
                        ["CSV", "JSON", "Parquet"] if file_type == "xlsx" else 
                        ["CSV", "JSON", "Excel (XLSX)"]
            )
            if st.button(f"Convert `{uploaded_file.name}`"):
                with st.spinner(f"Converting `{uploaded_file.name}` to `{target_format}`..."):
                    try:
                        output_file = convert_file(file_path, file_type, target_format)
                        conversion_history.append((uploaded_file.name, target_format, output_file.name))
                        st.success(f"✅ `{uploaded_file.name}` converted to `{output_file.name}`")
                        st.download_button(
                            label="📥 Download Converted File",
                            data=open(output_file, "rb").read(),
                            file_name=output_file.name,
                            mime="application/octet-stream"
                        )
                        cleanup_file(file_path)
                        cleanup_file(output_file)
                    except Exception as e:
                        st.error(f"❌ Error converting `{uploaded_file.name}`: {e}")
        st.session_state["conversion_history"] = conversion_history
    else:
        st.info("💡 Upload files to start the conversion process.")

def render_history():
    st.title("📜 Conversion History")
    history = st.session_state.get("conversion_history", [])
    if history:
        for original, target, converted in history:
            st.write(f"**{original}** ➡️ **{target}** ➡️ **{converted}**")
    else:
        st.info("No conversions yet.")

def layout():
    """Main layout and navigation for the app."""
    # Configure page layout
    st.set_page_config(page_title="File Conversion App", page_icon="🔄", layout="wide")

    # Sidebar navigation
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Conversion History"])

    # Render the selected page
    if page == "Home":
        render_home()
    elif page == "Conversion History":
        render_history()