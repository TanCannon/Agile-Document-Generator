import fitz  # PyMuPDF
import re
import csv

def extract_pdf_toc(input_pdf_path, output_heads_subheads) -> None:
    """
    Extract sections from a PDF based on headings and write them into an Excel file.
    
    Parameters:
    - input_pdf_path: str, path to the input PDF
    - output_csv_path: str, path to save the Excel output
    """
    
    # Open PDF
    doc = fitz.open(input_pdf_path)
    print(f"Total pages in PDF: {len(doc)}")
    
    # Dictionary to store headings, subheadings and their page numbers
    heads_subheads = {}

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("blocks")  # extract text blocks (with position info)

        for b in blocks:
            text = b[4].strip()
            if not text:
                continue

            # # Detect headings by regex pattern (ALL CAPS or Title Style)
            # if re.match(r'^\d+\.\s+[A-Z0-9&][A-Z0-9&\s-]+$', text):
            #     if text not in contents:
            #         contents[text] = []
            #     contents[text].append(page_num + 1)  # +1 because pages are 0-based
            
            # Detect both headings and subheadings by regex pattern (ALL CAPS or Title Style)
            if re.match(r'^\d+(?:\.\d+)*\.\s*[A-Z0-9&][A-Z0-9&\s-]*[A-Z][A-Z0-9&\s-]*$', text):
                if text not in heads_subheads:
                    heads_subheads[text] = []
                heads_subheads[text].append(page_num + 1)  # +1 because pages are 0-based
    # check if heads_subheads is empty
    if (heads_subheads == {}):
        print("No headings and subheadings found!!!")
    else:
        #save the whole list of headings and subheadings somewhere
        with open(output_heads_subheads, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter="|")
            writer.writerow(["Heads/Subheads", "Pages"])
            print("Detected both Headings and Subheadings:")
            for heading, pages in heads_subheads.items():
                print(f"{heading} -> {pages}")
                writer.writerow([heading, pages])
        print(f"PDF heading and subheading are succesfully written to {output_heads_subheads}")

def get_header_content(input_pdf_path: str, start_heading_name: str, start_page: int) -> str:
    # Open PDF
    doc = fitz.open(input_pdf_path)
    # Collect just the target headings content from start_page → end_page
    start_reading = 0
    end_reading = 0
    header_content = ""
    for page_num in range(start_page-1, len(doc)):
        if (end_reading == 1):
            break
        page = doc[page_num]
        blocks = page.get_text("blocks")
        
        for b in blocks:
            # y0 = b[1]
            text = b[4].strip()
            
            if text == start_heading_name:
                header_content += text + "\n"
                start_reading = 1
                continue

            if not text or start_reading == 0:
                continue

            # # Skip text above heading on start page
            # if page_num == start_page and y0 <= start_y:
            #     header_content += text + "\n"
            #     continue
            # Skip text below next heading on end page
            
            # if page_num == end_page and next_heading:
            #     continue
            # Detect both headings and subheadings by regex pattern (ALL CAPS or Title Style)
            if re.match(r'^\d+(?:\.\d+)*\.\s*[A-Z0-9&][A-Z0-9&\s-]*[A-Z][A-Z0-9&\s-]*$', text):
                # print(text)
                end_reading = 1
                break
            # print(f"text: {text}")
            header_content += text + "\n"

    doc.close()
    
    return header_content

def extract_from_csv_and_write(input_pdf_path, input_csv, output_csv):
    """
    Reads CSV line by line, extracts PDF content,
    and writes results to output CSV immediately.
    Works without hardcoding column names (assumes first col=heading, second col=page).
    """
    #empty output_csv
    with open(output_csv, "w", newline="", encoding="utf-8") as outfile:
        pass
    
    #read and write simultaneously
    with open(input_csv, "r", encoding="utf-8") as infile, \
        open(output_csv, "a", newline="", encoding="utf-8") as outfile:

        reader = csv.reader(infile, delimiter="|")
        headers = next(reader)  # grab header row dynamically
        heading_col, page_col = 0, 1  # assume first col = heading, second col = page

        # writer = csv.writer(outfile, delimiter="|")
        # writer.writerow(["Heading", "Content"])  # fixed output schema

        rows = list(reader)
        doc = fitz.open(input_pdf_path)

        for idx, row in enumerate(rows):
            start_heading = row[heading_col].strip()
            start_page = int(row[page_col].strip("[]"))
            content = get_header_content(input_pdf_path, start_heading, start_page)
            # writer.writerow([content])
            outfile.write(content)

        doc.close()

    print(f"Data of Headings of {input_csv} extracted to {output_csv}")

if __name__ == "__main__":
    # Example usage
    input_pdf = "./documents/DIG-ITS FRD_v2.pdf"
    output_csv = "./data/raw.csv"
    output_heads_subheads = "./data/raw/heads-subheads.csv"
    # extract_pdf_toc(input_pdf, output_heads_subheads)
    # print(f"PAGE_CONTENT = {get_header_content(input_pdf,"3.1 MENU STRUCTURE", 5)}")
    input_csv = "./outputs/answers-headings1.csv"
    output_csv = "./data/raw/extracted_contents.csv"

    extract_from_csv_and_write(input_pdf, input_csv, output_csv)
