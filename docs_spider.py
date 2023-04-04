from PyPDF2 import PdfReader
import argparse
import os


def main(pdf):
    file_name = os.path.basename(pdf)
    this_doc_id = file_name.split("_")[0]
    reader = PdfReader(pdf)
    for page in reader.pages:
        for line in page.extract_text(0).split("\n"):
            if line.startswith("DOC"):
                doc_id = line.split(":")[0].replace("DOC", "")
                print(f"{this_doc_id}, {doc_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", help="PDF file to read")
    args = parser.parse_args()
    main(args.pdf)
