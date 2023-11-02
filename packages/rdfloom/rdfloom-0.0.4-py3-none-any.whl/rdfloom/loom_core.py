import ipywidgets as widgets
from IPython.display import display

def in_jupyter():
    """Check if the code is running in a Jupyter Notebook."""
    if 'ipykernel' not in sys.modules:
        return True
    else:
        return False
def upload_files(allowed_extensions=['.xlsx', '.xls', '.csv', '.tsv']):
    """
    Function to upload files with specific extensions within a Jupyter Notebook.

    Parameters:
    - allowed_extensions (list): A list of string extensions to restrict the upload to specific file types.

    Returns:
    - A dictionary with filenames as keys and the binary content as values if successful, None otherwise.
    """
    uploader = widgets.FileUpload(
        accept=', '.join(allowed_extensions),
        multiple=False
    )

    display(uploader)

    uploaded_files = {}

    def on_upload_change(change):
        if change['name'] == 'data':
            # Process the files
            for filename, file_info in uploader.value.items():
                if any(filename.endswith(ext) for ext in allowed_extensions):
                    uploaded_files[filename] = file_info['content']
                    print(f"Uploaded '{filename}' ({len(file_info['content'])} bytes).")
                else:
                    print(f"File '{filename}' is not a supported format.")

    uploader.observe(on_upload_change, names='_counter')

    return uploaded_files