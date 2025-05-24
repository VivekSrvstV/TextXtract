from parsel import Selector
from playwright.sync_api import sync_playwright
from datetime import datetime
import csv
import json

class RGP:
    publications = []
    def scrape_researchgate_publications(query):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=50)
            page = browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")
            data = []
            page_num = 1
            print("----------------check 1------------------------------------")
            print(query)
            while True:
                page.goto(f"https://www.researchgate.net/search/publication?q={query}&page={page_num}")
                selector = Selector(text=page.content())

                for publication in selector.css(".nova-legacy-c-card__body--spacing-inherit"):
                    title = publication.css(
                        ".nova-legacy-v-publication-item__title .nova-legacy-e-link--theme-bare::text").get().title()
                    title_link = f'https://www.researchgate.net{publication.css(".nova-legacy-v-publication-item__title .nova-legacy-e-link--theme-bare::attr(href)").get()}'
                    publication_type = publication.css(".nova-legacy-v-publication-item__badge::text").get()
                    publication_date = publication.css(
                        ".nova-legacy-v-publication-item__meta-data-item:nth-child(1) span::text").get()
                    publication_doi = publication.css(
                        ".nova-legacy-v-publication-item__meta-data-item:nth-child(2) span").xpath(
                        "normalize-space()").get()
                    publication_isbn = publication.css(
                        ".nova-legacy-v-publication-item__meta-data-item:nth-child(3) span").xpath(
                        "normalize-space()").get()
                    authors = publication.css(".nova-legacy-v-person-inline-item__fullname::text").getall()
                    source_link = f'https://www.researchgate.net{publication.css(".nova-legacy-v-publication-item__preview-source .nova-legacy-e-link--theme-bare::attr(href)").get()}'
                    RGP.publications.append({
                        "title": title,
                        "link": title_link,
                        "source_link": source_link,
                        "publication_type": publication_type,
                        "publication_date": publication_date,
                        "publication_doi": publication_doi,
                        "publication_isbn": publication_isbn,
                        "authors": authors
                    })
                    data.append({
                        "title": title,
                        "link": title_link,
                        "authors": authors,
                        "publication_date": publication_date,
                        "publication_doi": publication_doi
                    })
                print(f"page number RGP : {page_num}")
                # checks if next page arrow key is greyed out `attr(rel)` (inactive) and breaks out of the loop
                if selector.css(".nova-legacy-c-button-group__item:nth-child(9) a::attr(rel)").get():
                    #print("here if")
                    break
                else:
                    #print("here else")
                    page_num += 1
                    if (page_num == 10):
                        break
            print(json.dumps(data, indent=2, ensure_ascii=False))
            # Serializing json
            json_object = json.dumps(RGP.publications, indent=4)

            # Writing to sample.json
            with open("../data/sample_rgp.json", "w") as outfile:
                outfile.write(json_object)
            browser.close()
            return data
    def csvpaste(data):
        #print('into csv')
        csv_columns = ["title","link","source_link","publication_type","publication_date","publication_doi","publication_isbn","authors"]
        dict_data = RGP.publications
        now = datetime.now()  # current date and time
        date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
        #print("date and time:", date_time)
        filename = date_time+"research_gate.csv"
        try:
            with open(filename, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in dict_data:
                    writer.writerow(d)
        except IOError:
            print("I/O error")

        #print(json.dumps(RGP.publications, indent=2, ensure_ascii=False))

