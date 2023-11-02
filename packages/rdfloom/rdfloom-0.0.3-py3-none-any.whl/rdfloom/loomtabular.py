import xlsxwriter
import pandas as pd
import sys
import ipywidgets as widgets
from IPython.display import display



def in_jupyter():
    """Check if the code is running in a Jupyter Notebook."""
    if 'ipykernel' not in sys.modules:
        return True
    else:
        return False


# file_uploader.py

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

def clean_column_names(columns: pd.Index) -> pd.Index:
    """Clean column names by performing various string operations."""
    return (columns.str.strip()
                  .str.lower()
                  .str.replace("  ", " ")
                  .str.replace(' ', '_')
                  .str.replace('(', '')
                  .str.replace(')', '')
                  .str.replace('\n', '_'))

def filter_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove columns containing the substring 'unnamed:'."""
    return df.loc[:, ~df.columns.str.contains('unnamed:', case=False)]

def clean_excel_data(input_filename: str) -> str:
    """
    Clean the given Excel file and save the cleaned data to a new Excel file.

    Args:
    - input_filename (str): The name of the Excel file (with the .xlsx extension) to be cleaned.

    Returns:
    - output_filename (str): The name of the cleaned Excel file.
    """

    # Extract base name from the input filename to use for the output filename
    base_name = input_filename.split('.')[0]
    output_filename = base_name + "_cleaned.xlsx"

    # Read the Excel file into a dictionary of DataFrames
    xls = pd.read_excel(input_filename, sheet_name=None)

    # Create a new Excel file for writing
    with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
        for sheet_name, df in xls.items():
            if sheet_name == 'Export Summary':
                continue
            df = filter_unnamed_columns(df)
            df.columns = clean_column_names(df.columns)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    return output_filename

def generate_metadata_entry_spreadsheet(cleaned_filename: str):
    """Generate metadata entry spreadsheet from cleaned Excel data."""
    xls = pd.read_excel(cleaned_filename + ".xlsx", sheet_name=None)

    # Data validation options
    semtypes_dropdown_data = ['categorical', 'string', 'integer', 'decimal', 'date']

    metaes = xlsxwriter.Workbook(cleaned_filename + '_metadata.xlsx')
    header_format = metaes.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#4F81BD', 'border': 1, 'align': 'center', 'valign': 'vcenter'})

    default_column_width = 15  # Adjust this value as needed

    for sheet, df in xls.items():
        if isinstance(df.columns, pd.core.indexes.range.RangeIndex):
            continue

        df.columns = clean_column_names(df.columns)
        currentsheet = metaes.add_worksheet(sheet)
        currentsheet.write(0, 0, 'Parameter', header_format)
        # ... [other setup code as you provided]

        for i in range(len(df.columns)):
            currentsheet.write(0, i + 1, df.columns[i], header_format)
            cell_reference = xlsxwriter.utility.xl_rowcol_to_cell(1, i + 1)
            currentsheet.data_validation(cell_reference, {'validate': 'list', 'source': semtypes_dropdown_data, 'input_title': 'Data type', 'input_message': 'Select a data type'})
            cell_reference = xlsxwriter.utility.xl_rowcol_to_cell(5, i + 1)
            ebi_ols_url = 'https://www.ebi.ac.uk/ols4/search?q=' + str(df.columns[i]).replace('_', '%20')
            currentsheet.write_url(cell_reference, ebi_ols_url, string=str(df.columns[i]))

        currentsheet.set_column(0, len(df.columns), default_column_width)
        for i, col in enumerate(df.columns):
            max_col_width = max(len(str(col)), df[col].astype(str).apply(len).max()) + 2
            if max_col_width > default_column_width:
                currentsheet.set_column(i + 1, i + 1, max_col_width)

    metaes.close()
    print("Metadata entry spreadsheet generated successfully!")