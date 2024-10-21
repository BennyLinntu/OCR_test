# here we import packages
import re
import pandas as pd
import pdfplumber
import os
import PyPDF2


# PDF file path
pdf_path = "Measuring-Emissions-Guidance_EmissionFactors_Summary_2023_ME1781.pdf"


def table_prextracted():
    tables_extracted = {}
    current_table_title = None
    current_table_data = []

    # Use pdfplumber to open PDF files
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]

            # Extract the table on the page
            page_tables = page.extract_tables()

            # Extract the page text to find the table title
            text = page.extract_text() if page.extract_text() else ""

            # Use regular expressions to extract table titles
            table_title_pattern = re.compile(r'Table\s\d+:\s.*')
            title_matches = table_title_pattern.findall(text)

            # Keep track of tables extracted from the current page
            table_title_idx = 0

            for table in page_tables:
                if table is None:
                    continue

                # Convert the table to a DataFrame for easier processing
                df = pd.DataFrame(table)

                # Skip empty or invalid forms
                if df.isnull().all(axis=None) or len(df.dropna()) < 2:
                    continue

                # Determine the form title
                if title_matches and table_title_idx < len(title_matches):
                    # If a new header is found, save the previous table data
                    if current_table_title and current_table_data:
                        combined_df = pd.concat(current_table_data, ignore_index=True)
                        tables_extracted[current_table_title] = combined_df

                    # Update the current table header and reset the table data list
                    current_table_title = title_matches[table_title_idx].strip()
                    current_table_data = []
                    table_title_idx += 1

                # Adds the current table to the list of tables under the current heading
                current_table_data.append(df)

            # If there is unsaved table data at the end of the page
            if current_table_title and current_table_data:
                combined_df = pd.concat(current_table_data, ignore_index=True)
                tables_extracted[current_table_title] = combined_df

    # Clean up and save each table as a separate Excel file
    current_directory = os.getcwd()
    output_directory = os.path.join(current_directory, 'Extracted_Tables')

    # If the directory doesn't exist, create it
    os.makedirs(output_directory, exist_ok=True)

    saved_table_names = []

    # # Save each table as an Excel file
    for title, df_table in tables_extracted.items():
        if df_table.shape[0] > 1:
            headers = df_table.iloc[0].fillna('').str.strip()
            df_table.columns = headers
            df_table = df_table.iloc[1:]


        df_table = df_table.loc[:, df_table.apply(lambda col: col.astype(str).str.strip().ne('').any(), axis=0)]


        df_table = df_table.loc[~df_table.apply(lambda row: row.astype(str).str.strip().eq('').all(), axis=1)]


        df_table.fillna('', inplace=True)


        df_table.reset_index(drop=True, inplace=True)


        valid_title = re.sub(r'[\\/*?:"<>|]', "_", title)


        excel_file_path = os.path.join(output_directory, f"{valid_title}.xlsx")
        df_table.to_excel(excel_file_path, index=False)


        saved_table_names.append(valid_title)

    output_file_path = os.path.join(output_directory, "Table_Names_From_Excel.txt")
    # Save all Excel filenames to a txt file
    with open(output_file_path, 'w') as file:
        for table_name in saved_table_names:
            file.write(table_name + "\n")
    # here we just print it's works or not
    print(f"Tables saved in: {output_directory}")
    print(f"Table names saved to {output_file_path}")


if __name__ == "__main__":
    table_prextracted()

