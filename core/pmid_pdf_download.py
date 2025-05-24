import os
from Bio import Entrez
from urllib.request import urlretrieve
from io import StringIO, BytesIO
class PMFDownnload:
    def downloadpdf(self):
        # Replace with your own email
        Entrez.email = "viveksriv19@gmail.com"
        # Set the filename of the text file containing the PMIDs
        filename = "../lib/PMF.txt"

        folder_path = "../fetched_pdfs/"
        import requests
        import os

        # Create a folder for the downloaded PDF files
        folder_path = '../fetched_pdfs'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Read pmids from a text file
        with open("../lib/PMF.txt") as f:
            pmids = [line.strip() for line in f]

        # Use Entrez E-utilities API to retrieve PMC IDs for each pmid
        pmc_ids = []
        for pmid in pmids:
            url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id={pmid}&db=pmc"
            response = requests.get(url)
            if response.ok:
                pmc_id = response.text.split('<Link><Id>')[1].split('</Id></Link>')[0]
                pmc_ids.append(pmc_id)

        # Use PMC Open Access Subset API to download PDF files for each PMC ID
        for pmc_id in pmc_ids:
            url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={pmc_id}&format=pdf"
            response = requests.get(url)
            if response.ok:
                # Save PDF file with pmc_id as filename in the "fetched_pdfs" folder
                file_path = os.path.join(folder_path, f"{pmc_id}.pdf")
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"Saved PDF file for PMC ID {pmc_id} to {file_path}")
            else:
                print(f"Failed to download PDF file for PMC ID {pmc_id}")
