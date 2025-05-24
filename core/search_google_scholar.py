from bs4 import BeautifulSoup
import requests, lxml, os, json
from parsel import Selector


class gScholar:

    @staticmethod
    def google_scholar_pagination(texts):
        #print(texts)
        # https://requests.readthedocs.io/en/latest/user/quickstart/#custom-headers
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }

        # https://requests.readthedocs.io/en/latest/user/quickstart/#passing-parameters-in-urls
        params = {
            # 'q': 'samsung medical center seoul semiconductor element simulation x-ray fetch',
            'q': texts,
            'hl': 'en',  # language of the search
            'start': 0  # page number ⚠
        }
        proxies = {
            'http': os.getenv('HTTP_PROXY')  # Or just type without os.getenv()
        }

        # JSON data will be collected here
        data = []

        while True:
            html = requests.get('https://scholar.google.com/scholar', headers=headers, params=params, proxies=proxies).text
            selector = Selector(text=html)
            #print(html)
            #print(f'extrecting {params["start"] + 10} page...')

            # Container where all needed data is located
            for result in selector.css('.gs_r.gs_or.gs_scl'):
                title = result.css('.gs_rt').xpath('normalize-space()').get()
                title_link = result.css('.gs_rt a::attr(href)').get()
                publication_info = result.css('.gs_a').xpath('normalize-space()').get()
                snippet = result.css('.gs_rs').xpath('normalize-space()').get()
                cited_by_link = result.css('.gs_or_btn.gs_nph+ a::attr(href)').get()

                data.append({
                    'page_num': params['start'] + 10,  # 0 -> 1 page. 70 in the output = 7th page
                    'title': title,
                    'title_link': title_link,
                    'publication_info': publication_info,
                    'snippet': snippet,
                    'cited_by_link': f'https://scholar.google.com{cited_by_link}',
                })

            # check if the "next" button is present
            if selector.css('.gs_ico_nav_next').get():
                params['start'] += 10
            else:
                break

        #print(json.dumps(data, indent=2, ensure_ascii=False))
        return data


# Part of the output:

'''
extrecting 10 page...
extrecting 20 page...
extrecting 30 page...
extrecting 40 page...
extrecting 50 page...
extrecting 60 page...
extrecting 70 page...
extrecting 80 page...
extrecting 90 page...
[
  {
    "page_num": 10,
    "title": "Comparative analysis of root canal filling debris and smear layer removal efficacy using various root canal activation systems during endodontic retreatment",
    "title_link": "https://www.mdpi.com/891414",
    "publication_info": "SY Park, MK Kang, HW Choi, WJ Shon - Medicina, 2020 - mdpi.com",
    "snippet": "… According to a recent study, the GentleWave System was effective in retrieving separated … Energy dispersive X-ray spectroscopy (EDX) may be used for the microchemical analysis of …",
    "cited_by_link": "https://scholar.google.com/scholar?cites=5221326408196954356&as_sdt=2005&sciodt=0,5&hl=en"
  },
  {
    "page_num": 90,
    "title": "Αυτόματη δημιουργία ερωτήσεων/ασκήσεων για εκπαιδευτικό σύστημα διδασκαλίας τεχνητής νοημοσύνης",
    "title_link": "http://nemertes.lis.upatras.gr/jspui/handle/10889/9424",
    "publication_info": "Ν Νταλιακούρας - 2016 - nemertes.lis.upatras.gr",
    "snippet": "Στόχος της διπλωματικής είναι ο σχεδιασμός ,η ανάπτυξη και υλοποίηση ενός συστήματος παραγωγής ερωτήσεων/ασκήσεων από κείμενα φυσικής γλώσσας. Κύριος στόχος των …",
    "cited_by_link": "https://scholar.google.com/scholar?q=related:1ovrKI-7xtUJ:scholar.google.com/&scioq=samsung+medical+center+seoul+semiconductor+element+simulation+x-ray+fetch&hl=en&as_sdt=0,5",
  }
]
'''
