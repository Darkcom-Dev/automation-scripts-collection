#!/usr/bin/env python3

import PyPDF2
# from PIL import Image
import argparse

def get_info(file):
    with open(file, 'rb') as f:
        pdfile = PyPDF2.PdfReader(f)
        info = pdfile.metadata
        number_of_pages = len(pdfile.pages)
        print(info)
        print(f'title: {info.title}')
        print(f'author: {info.author}')
        print(f'subject: {info.subject}')
        print(f'creator: {info.creator}')
        print(f'producer: {info.producer}')
        print(number_of_pages)


def version():
    print(f'argparse version: {argparse.__version__}')
    print(f'PyPDF2 version: {PyPDF2.__version__}')

parser = argparse.ArgumentParser(description="Split or Join PDF")

def extract_images_from_pdf(pdf_path, output_folder):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        resources = page['/Resources']
        for obj in resources:
            print(resources[obj])
            if '/ImageB' in resources[obj]:
                xObject = resources[obj][0]
                print(xObject)
                for image_key in xObject:
                    # print(xObject[image_key])
                    """ if xObject[image_key]['/Subtype'] == '/Image':
                        image = xObject[image_key]
                        image_data = image.get_object()
                        if isinstance(image_data, PyPDF2.generic.ByteStringObject):
                            with open(f'{output_folder}/image{page_num}_{image_key}.jpg', 'wb') as image_file:
                                image_file.write(image_data) """

    pdf_file.close()


def extract_image(file, output):
    # Extract images from a PDF file
    with open(file, "rb") as f:
        pdfile = PyPDF2.PdfReader(f)
        images = pdfile.pages[0].extract_text()
        with open(output, "w") as f:
            f.write(images)

def save_part(pages, start, end, output_file):
    """
    Save a range of pages from a list of pages to a PDF file.

    Parameters:
        pages (list): A list of pages to be saved.
        start (int): The index of the first page to be saved.
        end (int): The index of the last page to be saved (exclusive).
        output_file (str): The path to the output PDF file.

    Returns:
        None
    """
    pdf_writer = PyPDF2.PdfWriter()

    for i in range(start, end):
        pdf_writer.add_page(pages[i])
    with open(output_file, "wb") as f:
        pdf_writer.write(f)

def split(file, page, *output):
    """
    Split a PDF file into two parts based on the given page number.

    Args:
        file (str): The path to the PDF file.
        page (int): The page number at which to split the PDF file.
        output (tuple): A tuple containing the paths to save the two parts of the PDF file.
    
    Returns:
        None
    """
    print("Splitting PDF")
    print(f'file: {file}, page: {page}')
    print(f'output: {output}')

    with open(file, "rb") as f:
        pdfile = PyPDF2.PdfReader(f)
        pages = pdfile.pages

        save_part(pages, 0, page, output[0])
        save_part(pages, page, len(pages), output[1])
"""
def convert_img_to_pdf(file, output):
    image = Image.open(file)
    image_rgb = image.convert('RGB')
    print(image.width, image.height)
    pdffile = PyPDF2.PdfWriter()
    page = pdffile.add_blank_page(width=image.width, height=image.height)
    page.merge_page(image)
    #pdffile.add_page(page)
    with open(output, 'wb') as f:
        pdffile.write(f)
"""
def join(output, *files):
    """
    Join multiple PDF files into a single PDF file.

    Parameters:
        output (str): The path of the output PDF file.
        *files (str): The paths of the input PDF files.

    Returns:
        None
    """
    print("Joining PDF")
    print(f'files: {files}')
    print(f'output: {output}')

    merger = PyPDF2.PdfMerger()
    for file in files:
        pdffile = PyPDF2.PdfReader(open(file,'rb'))
        merger.append(pdffile)

    with open(output, 'wb') as f:
        merger.write(f)

    merger.close()

parser.add_argument(
    "-i", "--input", nargs="+", help="Input PDF file(s)", required=True
)
parser.add_argument(
    "-o", "--output", nargs="+", help="Output PDF file(s)", required=True
)
parser.add_argument(
    "-s", "--split", help="Split PDF", action="store_true"
)
parser.add_argument(
    "-j", "--join", help="Join PDF", action="store_true"
)
parser.add_argument(
    "-c", "--convert", help="Convert image to PDF", action="store_true"
)
parser.add_argument(
    "-n", "--number", help="Number of pages to split", type=int
)
parser.add_argument(
    "-l", "--length", help="Length of each page", type=int
)
parser.add_argument(
    "-p", "--page", help="Page to split", type=int
)
parser.add_argument(
    "-v", "--version", action="version", version=version
)
parser.add_argument(
    "-g", "--get_info", action="store_true", help="Get info from PDF"
)
parser.add_argument(
    "-x", "--extract", action="store_true", help="Extract images from PDF"
)

args = parser.parse_args()
if args.split:
    if not args.output:
        print("Please specify an output file")
    if type(args.output) != list:
        print("Please specify an output file")
    if type(args.page) != int:
        print("Please specify a page integer")
    else:
        split(args.input[0], args.page, *args.output)
elif args.join:
    if not args.output:
        print("Please specify an output file")
    if type(args.output) != list:
        print("Please specify an output file")
    else:
        join(args.output[0], *args.input)
elif args.get_info:
    get_info(args.input[0])
elif args.extract:
    if not args.output:
        print("Please specify an output file")
    if type(args.output) != list:
        print("Please specify an output file")
    else:
        extract_images_from_pdf(args.input[0], args.output[0])
"""
elif args.convert:
    if not args.output:
        print("Please specify an output file")
        main()
    if type(args.output) != list:
        print("Please specify an output file")
        main()
    else:
        convert_img_to_pdf(args.input[0], args.output[0])
"""
