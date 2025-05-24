# Importing libraries
import requests
from bs4 import BeautifulSoup


class SearchesGoogle:

    @staticmethod
    def geturls(searchKey):

        # setting up the URL
        url = 'https://scholar.google.com/scholar?start=10&q=plant+preview&hl=en&as_sdt=0,5'

        # perform get request to the url
        reqs = requests.get(url)

        # extract all the text that you received from
        # the GET request
        content = reqs.text

        # convert the text to a beautiful soup object
        soup = BeautifulSoup(content, 'html.parser')

        # Empty list to store the output
        urls = []
        urlheads = []
        # For loop that iterates over all the <li> tags
        for h in soup.findAll('h3'):

            # looking for anchor tag inside the <li>tag
            a = h.find('a')
            texts = a.text.strip()
            urlheads.append(texts)
            try:

                # looking for href inside anchor tag
                if 'href' in a.attrs:
                    # storing the value of href in a separate variable
                    url = a.get('href')

                    # appending the url to the output list
                    urls.append(url)

            # if the list does not has a anchor tag or an anchor tag
            # does not has a href params we pass
            except:
                pass

        # print all the urls stored in the urls list
        return urls,urlheads
        #for url in urls:
        #    print(url)
        #    return urls
