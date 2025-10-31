import streamlit as st
from config.settings import settings
import io
import os
import zipfile
from scripts import runAllPrompts
from scripts import generateMockups
import time
from config.settings import settings

# define layouts
# col1, col2 = st.columns(2,vertical_alignment="bottom")
# -------------------------
# Utility: General ZIP function
# -------------------------
def make_zip_from_paths(paths, base_dir=None):
    """
    Create a ZIP archive from a list of files/folders.

    Args:
        paths (list[str]): List of file or folder paths to include in the zip.
        base_dir (str): Optional base directory. If set, relative paths inside
                        the zip will be relative to this directory.

    Returns:
        bytes: In-memory zip file (as bytes).
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for path in paths:
            if os.path.isfile(path):
                arcname = os.path.relpath(path, base_dir) if base_dir else os.path.basename(path)
                zipf.write(path, arcname)
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        filepath = os.path.join(root, file)
                        arcname = os.path.relpath(filepath, base_dir if base_dir else path)
                        zipf.write(filepath, arcname)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


# -------------------------
# App parameters
# -------------------------
app_title = "GAIG - POC"
st.title(app_title)

# Initialize session state
if "processed" not in st.session_state:
    st.session_state.processed = False
    st.session_state.uploaded_file_name = None
if "extra_done" not in st.session_state:
    st.session_state.extra_done = False


# -------------------------
# File Upload
# -------------------------
uploaded_file = st.file_uploader("Upload Project FRD", type=["txt", "pdf", "csv", "docx"])

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    save_path = f"./uploades/saved_{uploaded_file.name}"

    # Save and process only if new file is uploaded
    if st.session_state.uploaded_file_name != uploaded_file.name:
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        st.session_state.uploaded_file_name = uploaded_file.name
        st.session_state.generated_docs = False
        st.session_state.generated_mockups= False  # reset extra work too

        # st.info(f"File saved locally as: {save_path}")

        # Run generate docs only once per uploaded file
    tab1, tab2 = st.tabs(["Generate Documents", "Generate UI Mockups"])
    with tab1:
        if st.button("Generate Documents"):
            if not st.session_state.generated_docs:
                start = time.time()
                with st.spinner("Generating documents...", show_time=True):
                    runAllPrompts.runAllPrompts(save_path)
                    print("ran runAllPrompts.runAllPrompts(save_path)")
                total = time.time() - start
                st.success(f"Generated docs in {total:2f} seconds.")
                st.session_state.generated_docs = True
            else:
                st.warning("Documents already generated for this file")

        if st.session_state.generated_docs:
                # -------------------------
            # Download Options
            # -------------------------
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
                data = make_zip_from_paths([
                    settings.output_file1_xlsx,
                    settings.output_file2_xlsx,
                    settings.output_file3_xlsx
                ])
                filename = f"All_Documents_{uploaded_file.name}.zip"

            # -------------------------
            # Download Button
            # -------------------------
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
            
    with tab2:
        # Run generate mockups only once per uploaded file
        if st.button("Generate UI Mockups"):
            if not st.session_state.generated_mockups:
                with st.spinner("Running extra task and preparing ZIP...", show_time=True):
                    start = time.time()

                    # Generate mockups
                    # def main(input_pdf_path: str, output_heads_subheads: str = settings.output_heads_subheads):
                    generateMockups.main(save_path)
                    print("ran generateMockups.main(save_path)")

                    total = time.time() - start
                    st.success(f"Generated mockups in {total:2f} seconds.")

                    #lock this generateMockups function call
                    st.session_state.generated_mockups = True
            else: 
                st.warning("UI mockups already generated for this file")
            
        if st.session_state.generated_mockups: 
            extra_folders = [settings.screenshot_output_path]
            # Create ZIP of the extra work
            data = make_zip_from_paths(extra_folders)
            if data:
                st.download_button(
                    label="Download Mockups (ZIP)",
                    data=data,
                    file_name=f"UI_Mockups{uploaded_file.name}.zip",
                    mime="application/zip"
                )
