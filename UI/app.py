import streamlit as st
from config.settings import settings
import io
import zipfile
from scripts import runAllPrompts
import os

# app parameters
app_title = "GAIG - POC"

st.title(app_title)

# Initialize session state for processing
if "processed" not in st.session_state:
    st.session_state.processed = False
    st.session_state.uploaded_file_name = None

# Upload button
uploaded_file = st.file_uploader("Upload Project FRD", type=["txt", "pdf", "csv", "docx"])

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    # Save locally
    save_path = f"./uploades/saved_{uploaded_file.name}"

    # Save only if new file is uploaded
    if st.session_state.uploaded_file_name != uploaded_file.name:
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        st.session_state.uploaded_file_name = uploaded_file.name
        st.session_state.processed = False  # reset flag

    st.info(f"File saved locally as: {save_path}")

    # Run processing only once
    if not st.session_state.processed:
        with st.spinner("Generating documents...", show_time=True):
            runAllPrompts.runAllPrompts(save_path)
        st.session_state.processed = True

    # Dropdown for downloads
    option = st.selectbox(
        "Choose document to download:",
        ["All Documents (ZIP)", "User Stories", "Sprint Planning", "Gantt Chart"]
    )

    data, filename = None, None

    if option == "User Stories":
        with open(settings.output_file1_xlsx, "rb") as f1:
            data = f1.read()
        filename = f"User_Stories_{uploaded_file.name}.xlsx"

    elif option == "Sprint Planning":
        with open(settings.output_file2_xlsx, "rb") as f1:
            data = f1.read()
        filename = f"Sprint_Planning_{uploaded_file.name}.xlsx"

    elif option == "Gantt Chart":
        with open(settings.output_file3_xlsx, "rb") as f1:
            data = f1.read()
        filename = f"Gantt_Chart_{uploaded_file.name}.xlsx"

    elif option == "All Documents (ZIP)":
        # Create an in-memory ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(settings.output_file1_xlsx, f"User_Stories_{uploaded_file.name}.xlsx")
            zipf.write(settings.output_file2_xlsx, f"Sprint_Planning_{uploaded_file.name}.xlsx")
            zipf.write(settings.output_file3_xlsx, f"Gantt_Chart_{uploaded_file.name}.xlsx")
        zip_buffer.seek(0)
        data = zip_buffer.getvalue()
        filename = f"All_Documents_{uploaded_file.name}.zip"

    # Show download button
    if data:
        mime_type = (
            "application/zip"
            if filename.endswith(".zip")
            else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.download_button(
            label=f"Download {option}",
            data=data,
            file_name=filename,
            mime=mime_type
        )
