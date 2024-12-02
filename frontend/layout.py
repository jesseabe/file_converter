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

def layout():
    # Page configuration
    st.set_page_config(page_title="File Conversion App", page_icon="🔄", layout="wide")

    # Sidebar for navigation
    st.sidebar.header("File Conversion App")
    st.sidebar.write(
        """
        Upload your file, select the desired conversion format, 
        and download the converted file easily. 🛠️
        """
    )

    # Main interface
    st.title("🌟 File Conversion App 🌟")
    st.markdown(
        """
        Welcome to the **File Conversion App**. This tool allows you to convert files between formats 
        (CSV, JSON, XLSX, Parquet) seamlessly. 📂
        """
    )

    # File upload
    uploaded_file = st.file_uploader(
        "Upload a file for conversion:", 
        type=["csv", "json", "xlsx", "parquet"],
        help="Supported formats: CSV, JSON, XLSX, Parquet."
    )

    if uploaded_file:
        # Display file details
        st.success(f"📄 File uploaded: `{uploaded_file.name}`")
        save_path = UPLOAD_FOLDER / uploaded_file.name

        # Save the uploaded file
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Define conversion options
        file_type = uploaded_file.name.split(".")[-1].lower()
        conversion_options = {
            "csv": ["JSON", "Excel (XLSX)", "Parquet"],
            "json": ["CSV", "Excel (XLSX)", "Parquet"],
            "xlsx": ["CSV", "JSON", "Parquet"],
            "parquet": ["CSV", "JSON", "Excel (XLSX)"],
        }

        # Display conversion options
        st.subheader("Conversion Options")
        target_format = st.selectbox(
            "Select the target file format:",
            conversion_options.get(file_type, [])
        )

        if st.button("Convert"):
            output_file = None
            try:
                # Call appropriate conversion function
                if file_type == "csv":
                    if target_format == "JSON":
                        output_file = save_path.with_suffix(".json")
                        csv_to_json(save_path, output_file)
                    elif target_format == "Excel (XLSX)":
                        output_file = save_path.with_suffix(".xlsx")
                        csv_to_xlsx(save_path, output_file)
                    elif target_format == "Parquet":
                        output_file = save_path.with_suffix(".parquet")
                        csv_to_parquet(save_path, output_file)

                elif file_type == "json":
                    if target_format == "CSV":
                        output_file = save_path.with_suffix(".csv")
                        json_to_csv(save_path, output_file)
                    elif target_format == "Excel (XLSX)":
                        output_file = save_path.with_suffix(".xlsx")
                        json_to_xlsx(save_path, output_file)
                    elif target_format == "Parquet":
                        output_file = save_path.with_suffix(".parquet")
                        json_to_parquet(save_path, output_file)

                elif file_type == "xlsx":
                    if target_format == "CSV":
                        output_file = save_path.with_suffix(".csv")
                        xlsx_to_csv(save_path, output_file)
                    elif target_format == "JSON":
                        output_file = save_path.with_suffix(".json")
                        xlsx_to_json(save_path, output_file)
                    elif target_format == "Parquet":
                        output_file = save_path.with_suffix(".parquet")
                        xlsx_to_parquet(save_path, output_file)

                elif file_type == "parquet":
                    if target_format == "CSV":
                        output_file = save_path.with_suffix(".csv")
                        parquet_to_csv(save_path, output_file)
                    elif target_format == "JSON":
                        output_file = save_path.with_suffix(".json")
                        parquet_to_json(save_path, output_file)
                    elif target_format == "Excel (XLSX)":
                        output_file = save_path.with_suffix(".xlsx")
                        parquet_to_xlsx(save_path, output_file)

                if output_file:
                    st.success(f"✅ Conversion successful: `{output_file.name}`")
                    st.download_button(
                        label="📥 Download Converted File",
                        data=open(output_file, "rb").read(),
                        file_name=output_file.name,
                        mime="application/octet-stream"
                    )
                    # Cleanup files after download
                    cleanup_file(save_path)
                    cleanup_file(output_file)
            except Exception as e:
                st.error(f"❌ An error occurred during conversion: {e}")
    else:
        st.info("💡 Please upload a file to start the conversion process.")

