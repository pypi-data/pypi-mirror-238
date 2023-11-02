import os
from PyPDF2 import PdfReader, PdfWriter
import datetime as dt


def split_pdf(file_path: str,
              file_base_name: str = None,
              output_dir: str = None) -> None:
    """
    This function splits a multi-page PDF into it's individual pages.
    :param file_path: file path of the pdf
    :param file_base_name: Base name of the separated files.
    :param output_dir: output directory
    :return: None
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # creates the output directory if it does not exist

    # Open the PDF file
    with open(file_path, 'rb') as file:
        pdf = PdfReader(file)

        # Iterate through each page in the PDF and save them separately in the output directory
        for page_number, page in enumerate(pdf.pages):

            # if no name is provided, use a generic name containing the date
            if file_base_name is None:
                file_base_name = dt.datetime.today().strftime("%Y_%m_%d") + "_page"
            output_file = os.path.join(output_dir,
                                       f"{file_base_name}_{page_number+1}.pdf")

            # Write the current page to the new file
            with open(output_file, 'wb') as output:
                writer = PdfWriter()
                writer.add_page(page)
                writer.write(output)
