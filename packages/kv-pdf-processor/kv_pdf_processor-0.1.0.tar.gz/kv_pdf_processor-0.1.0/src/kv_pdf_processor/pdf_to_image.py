import fitz
import os


def convert_pdf_to_jpeg(pdf_path: str,
                        output_dir: str,
                        base_name: str = "",
                        dpi: int = 300) -> None:
    """
    This file converts a single page pdf to a jpeg image
    :param pdf_path: File path of the PDF file to be converted to JPEG.
    :param output_dir: Folder directory to store the images
    :param base_name: the file name of the pdf (Optional)
    :param dpi: Image resolution in dots/inch
    :return: None
    """

    # Creates the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the PDF file using fitz
    with fitz.open(pdf_path) as doc:
        # Iterate through each page in the PDF
        for i, page in enumerate(doc):
            # Create a pixmap of the page with the specified DPI
            # TODO: Possible change of the matrix size
            pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))

            # Create the output JPEG file path
            if base_name == "":
                base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            jpeg_path = os.path.join(output_dir, f"{base_name}.jpeg")

            # Save the pixmap as JPEG
            pix.save(jpeg_path, "jpeg")
