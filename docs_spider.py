from PyPDF2 import PdfReader
from pyvis.network import Network
import networkx as nx
from selenium import webdriver
from selenium.webdriver.common.by import By


import argparse
import dotenv
import time
import os


def fetch_pdf_from_amsystem(url, username, password):
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(5)  # Let the user actually see something!
    username_input = driver.find_element(by=By.NAME, value="username")
    username_input.send_keys(username)

    password_input = driver.find_element(by=By.NAME, value="password")
    password_input.send_keys(password)

    submit_btn = driver.find_element(by=By.ID, value="submit")
    submit_btn.click()

    driver.quit()


def extract_from_pdf(pdf, nodes, edges):
    file_name = os.path.basename(pdf)
    this_doc_id = f'DOC{file_name.split("_")[0]}'
    reader = PdfReader(pdf)

    if this_doc_id not in nodes:
        nodes.add(this_doc_id)

    for page in reader.pages:
        for line in page.extract_text(0).split("\n"):
            if line.startswith("DOC"):
                doc_id = line.split(":")[0]
                print(f"{this_doc_id}, {doc_id}")

                if doc_id not in nodes:
                    nodes.add(doc_id)
                edges.add((this_doc_id, doc_id))

    return nodes, edges


def main(pdf):
    dotenv.load_dotenv()
    url = os.getenv("DOCS_SPIDER_URL")
    username = os.getenv("DOCS_SPIDER_USERNAME")
    password = os.getenv("DOCS_SPIDER_PASSWORD")
    fetch_pdf_from_amsystem(url, username, password)
    nodes = set()
    edges = set()

    nodes, edges = extract_from_pdf(pdf, nodes, edges)

    net = Network()
    net.add_nodes(nodes)
    net.add_edges(edges)
    net.write_html("docs.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", help="PDF file to read")
    args = parser.parse_args()
    main(args.pdf)
