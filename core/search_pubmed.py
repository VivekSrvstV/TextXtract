import os
import shutil

from parsel import Selector
from playwright.sync_api import sync_playwright
from datetime import datetime
import csv
import json
import re
import requests

class SPM:
    publications = []

    def scrape_pubmed_publications(query):
        SPM.publications.clear()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=50)
            page = browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")

            data = []
            listObj = []
            page_num = 1
            now = datetime.now()
            s1 = now.strftime("%m/%d/%Y, %H:%M:%S")

            while True:
                # page.goto(f"https://pubmed.ncbi.nlm.nih.gov/?term=(plant%5BTitle%5D)%20AND%20(phenomics%5BTitle%2FAbstract%5D)&sort=&page=1")
                page.goto(f"https://pubmed.ncbi.nlm.nih.gov?term={query}&page={page_num}")
                #selector = Selector(text=page.content())
                response = requests.get(f"https://pubmed.ncbi.nlm.nih.gov?term={query}&page={page_num}")
                selector = Selector(text=page.content())
                total_results = selector.css(".value::text").get()

                selector1 = Selector(response.text)
                url1 = response.url
                print("url of the page----", url1)
                print("query is ------", query)
                if '?term=' in url1:
                    last_page = selector.css(".of-total-pages::text").get()
                    print("The list after Extracting numbers : ")
                    print("----------total result---------------")
                    print(total_results)
                    print(last_page)
                    while "," in total_results:
                        total_results = total_results.replace(",", "")
                    total_results = int(total_results)
                    if (int(total_results) > 10):
                        lpage = int(total_results) / 10
                    else:
                        lpage = 1

                    print("the last page is " + str(lpage))

                    listObj.append({
                        "Query": query,
                        "Results": total_results,
                        "Time": s1
                    })


                    # iterate over the selected divs and extract the desired data
                    divs = selector.css('.docsum-content:not(.top-citations)')

                    for publication in selector.css('.docsum-content:not(.top-citations)'):
                        title = publication.css(".docsum-title").get()
                        title = re.sub("<.*?>", "", title)
                        title = title.strip()
                        title_link = f'https://pubmed.ncbi.nlm.nih.gov{publication.css(".docsum-title::attr(href)").get()}'
                        pmid = publication.css(".docsum-pmid::text").get()
                        authors = publication.css(".full-authors::text").get()
                        if(publication.css(".full-journal-citation::text")):
                            cite = publication.css(".full-journal-citation::text").get()
                            parts = cite.split(". ")

                            if (len(parts) > 2):
                                pub_doi = parts[2]
                            else:
                                pub_doi = ""
                            pub_name = parts[0]

                            pub_date = parts[1].split(";")[0]
                            if ';' in parts[1]:
                                version = parts[1].split(";")[1]

                        else:
                            print('into else')
                            authors = selector.css('div.docsum-citation span.docsum-authors::text').extract_first()
                            journal = selector.css(
                                'div.docsum-citation span.docsum-journal-citation::text').extract_first()
                            pmid = selector.css('div.docsum-citation span.docsum-pmid::text').extract_first()
                            cite = journal
                            pub_doi = pmid
                            pub_name = journal
                            version = ""
                            pub_date = ""


                        source_link = f'https://pubmed.ncbi.nlm.nih.gov{publication.css(".docsum-title::attr(href)").get()}'
                        SPM.publications.append({
                            "title": title,
                            "link": title_link,
                            "source_link": source_link,
                            "publication_date": pub_date,
                            "pmid": pmid,
                            "publication_doi": pub_doi,
                            "authors": authors,
                            "total_results": total_results,
                            "cite": cite,
                            "publication_name": pub_name,
                            "version": version
                        })
                        data.append({
                            "title": title,
                            "link": title_link,
                            "source_link": source_link,
                            "publication_date": pub_date,
                            "pmid": pmid,
                            "publication_doi": pub_doi,
                            "authors": authors,
                            "total_results": total_results,
                            "cite": cite,
                            "publication_name": pub_name,
                            "version": version
                        })

                    print(f"page number: {page_num}")
                    if selector.css('.button-wrapper next-page-btn:disabled').get():
                        break
                    else:
                        if (lpage == 1):
                            break
                        else:
                            page_num += 1
                            if (page_num == lpage or page_num > lpage):
                                print('i m here ',page_num)
                                print(int(lpage))
                                print(lpage)
                                break
                else:
                    print("in url")
                    html = response.text
                    sel = Selector(text=html)
                    h1_elem = sel.css('h1.heading-title')
                    t = h1_elem.xpath('text()').get()
                    ti = re.sub("<.*?>", "", t)
                    title = ti.strip()
                    print(title)
                    title_link = url1
                    print(title_link)
                    source_link = url1
                    pubdate = sel.css('span.cit')
                    # get the value of the span element
                    pub_date = pubdate.xpath('text()').get().split(';')[0]
                    print(pub_date)
                    pmid = sel.css('strong.current-id[title="PubMed ID"]').xpath('text()').get()
                    print(pmid)
                    a_elem = sel.css('a.id-link[target="_blank"]')
                    text_content = a_elem.xpath('text()').get()
                    href_value = a_elem.xpath('@href').get()
                    pub_doi = href_value.split('/')[-1]
                    print(pub_doi)

                    authors_l = []
                    unique_authors = set()
                    for author in sel.css('.authors-list-item'):
                        name = author.css('.full-name::text').get()
                        author_str = f"{name}"
                        if author_str not in unique_authors:
                            authors_l.append(author_str)
                            unique_authors.add(author_str)

                    authors = ", ".join(authors_l)
                    print(authors)
                    total_results = 1
                    cite = pubdate.xpath('text()').get().split(';')[1]
                    pubname = sel.css('button#full-view-journal-trigger').xpath('text()').get()
                    pn = re.sub("<.*?>", "", pubname)
                    pub_name = pn.strip()
                    print(pub_name)
                    version = 0
                    print('check here')
                    SPM.publications.append({
                        "title": title,
                        "link": title_link,
                        "source_link": source_link,
                        "publication_date": pub_date,
                        "pmid": pmid,
                        "publication_doi": pub_doi,
                        "authors": authors,
                        "total_results": total_results,
                        "cite": cite,
                        "publication_name": pub_name,
                        "version": version
                    })
                    data.append({
                        "title": title,
                        "link": title_link,
                        "source_link": source_link,
                        "publication_date": pub_date,
                        "pmid": pmid,
                        "publication_doi": pub_doi,
                        "authors": authors,
                        "total_results": total_results,
                        "cite": cite,
                        "publication_name": pub_name,
                        "version": version
                    })
                    break
                    print(data)
                    print(SPM.publications)
                    print('#########################################################################################')

            print(json.dumps(SPM.publications, indent=2, ensure_ascii=False))
            return data
    def csvpaste(data):
        print('into csv')
        SPM.deleteFilesFromFolder("csv_results")
        csv_columns = [
            "title",
            "link",
            "source_link",
            "publication_date",
            "pmid",
            "publication_doi",
            "authors",
            "total_results",
            "cite",
            "publication_name",
            "version"
        ]
        dict_data = SPM.publications
        now = datetime.now()  # current date and time
        date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
        print("date and time:", date_time)
        filename = date_time+"pubmed.xlsx"
        fileForData = "data.csv"
        try:
            with open("csv_results/"+filename, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in dict_data:
                    writer.writerow(d)
        except IOError:
            print("I/O error")
        SPM.deleteFilesFromFolder("data_results")
        try:
            with open("data_results/"+fileForData, 'w') as csvs:
                writer = csv.DictWriter(csvs, fieldnames=csv_columns)
                writer.writeheader()
                for d in dict_data:
                    writer.writerow(d)
        except IOError:
            print("I/O error")
        return dict_data
        #print(json.dumps(SPM.publications, indent=2, ensure_ascii=False))
    def deleteFilesFromFolder(self):
        folder = os.path.abspath(self)
        #folder_path = os.path.abspath(folder)
        #print(folder_path)

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    def write_to_pmf(self):
        print('into pmf')
        SPM.deleteFilesFromFolder("fetched_pdfs")
        dict_data = SPM.publications
        #pdfFiles = []
        try:
            with open("../lib/PMF", 'a') as file:
                file.seek(0)
                file.truncate()
                for d in dict_data:
                    #print(d)
                    #pdfFiles.append({"title": d["title"], "pmid": d["publication_doi"]})
                    file.write(d["pmid"]+"\n")
        except IOError:
            print("I/O error")
        #return pdfFiles

    def listFileWithTitle(self):
        folder = os.path.abspath('../fetched_pdfs')
        pdfFiles = []
        dict_data = SPM.publications
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                pdfFiles.append(filename)
                print(filename)
        print(pdfFiles)
        pmidlist = [x[:-4] for x in pdfFiles]
        result = []
        for i in pmidlist:
            print("inside pdf lists")
            print(i)
            for j in dict_data:
                print("inside dict data list")
                print(j["pmid"])
                if i == j["pmid"]:
                    print("value found")
                    result.append({ "pmid":j["pmid"], "title": j["title"]})
        return result