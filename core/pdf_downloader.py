

import argparse
import sys

import os
import requests
from bs4 import BeautifulSoup
import re
import urllib


parser = argparse.ArgumentParser()
parser._optionals.title = "Flag Arguments"
parser.add_argument('-pmids', help="Comma separated list of pmids to fetch. Must include -pmids or -pmf.",
                    default='%#$')
parser.add_argument('-pmf',
                    help="File with pmids to fetch inside, one pmid per line. Optionally, the file can be a tsv with a second column of names to save each pmid's article with (without '.pdf' at the end). Must include -pmids or -pmf",
                    default='%#$')
parser.add_argument('-out', help="Output directory for fetched articles.  Default: fetched_pdfs",
                    default="fetched_pdfs")
parser.add_argument('-errors', help="Output file path for pmids which failed to fetch.  Default: unfetched_pmids.tsv",
                    default="unfetched_pmids.tsv")
parser.add_argument('-maxRetries', help="Change max number of retries per article on an error 104.  Default: 3",
                    default=3, type=int)
args = vars(parser.parse_args())



if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    exit(1)
if args['pmids'] == '%#$' and args['pmf'] == '%#$':
    #print("Error: Either -pmids or -pmf must be used.  Exiting.")
    exit(1)
if args['pmids'] != '%#$' and args['pmf'] != '%#$':
    #print("Error: -pmids and -pmf cannot be used together.  Ignoring -pmf argument")
    args['pmf'] = '%#$'



if not os.path.exists(args['out']):
    print("Output directory of {0} did not exist.  Created the directory.".format(args['out']))
    os.mkdir(args['out'])


def getMainUrl(url):
    print("====================================check 17================================")

    return "/".join(url.split("/")[:3])


def savePdfFromUrl(pdfUrl, directory, name, headers):
    print("====================================check 16================================")

    t = requests.get(pdfUrl, headers=headers, allow_redirects=True)
    with open('{0}/{1}.pdf'.format(directory, name), 'wb') as f:
        f.write(t.content)


def fetch(pmid, finders, name, headers, errorPmids):
    print("====================================check 15================================")

    uri = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id={0}&retmode=ref&cmd=prlinks".format(
        pmid)
    success = False
    dontTry = False
    print(uri)
    if os.path.exists("{0}/{1}.pdf".format(args['out'], pmid)):  # bypass finders if pdf re#print already stored locally
        print("** Re#print #{0} already downloaded and in folder; skipping.".format(pmid))
        return
    else:
        # first, download the html from the page that is on the other side of the pubmed API
        req = requests.get(uri, headers=headers)
        if 'ovid' in req.url:
            print(" ** Re#print {0} cannot be fetched as ovid is not supported by the requests package.".format(pmid))
            errorPmids.write("{}\t{}\n".format(pmid, name))
            dontTry = True
            success = True
        soup = BeautifulSoup(req.content, 'lxml')
        #         return soup
        # loop through all finders until it finds one that return the pdf re#print
        if not dontTry:
            for finder in finders:
                print("Trying {0}".format(finder))
                pdfUrl = eval(finder)(req, soup, headers)
                if type(pdfUrl) != type(None):
                    savePdfFromUrl(pdfUrl, args['out'], name, headers)
                    success = True
                    print("** fetching of re#print {0} succeeded".format(pmid))
                    break

        if not success:
            print("** Re#print {0} could not be fetched with the current finders.".format(pmid))
            errorPmids.write("{}\t{}\n".format(pmid, name))



def acsPublications(req, soup, headers):
    print("====================================check 14================================")

    possibleLinks = [x for x in soup.find_all('a') if type(x.get('title')) == str and (
                'high-res pdf' in x.get('title').lower() or 'low-res pdf' in x.get('title').lower())]

    if len(possibleLinks) > 0:
        print("** fetching re##print using the 'acsPublications' finder...")
        pdfUrl = getMainUrl(req.url) + possibleLinks[0].get('href')
        return pdfUrl

    return None


def direct_pdf_link(req, soup, headers):  # if anyone has a PMID that direct links, I can debug this better
    print("====================================check 13================================")

    if req.content[-4:] == '.pdf':
        print("** fetching re##print using the 'direct pdf link' finder...")
        pdfUrl = req.content
        return pdfUrl

    return None



def futureMedicine(req, soup, headers):
    print("====================================check 12================================")

    possibleLinks = soup.find_all('a', attrs={'href': re.compile("/doi/pdf")})
    if len(possibleLinks) > 0:
        print("** fetching re##print using the 'future medicine' finder...")
        pdfUrl = getMainUrl(req.url) + possibleLinks[0].get('href')
        return pdfUrl
    return None


def genericCitationLabelled(req, soup,headers):  # if anyone has CSH access, I can check this.  Also, a PMID on CSH would help debugging
    print("====================================check 11================================")

    possibleLinks = soup.find_all('meta', attrs={'name': 'citation_pdf_url'})
    if len(possibleLinks) > 0:
        print("** fetching re##print using the 'generic citation labelled' finder...")
        pdfUrl = possibleLinks[0].get('content')
        return pdfUrl
    return None



def nejm(req, soup, headers):
    print("====================================check 10================================")

    possibleLinks = [x for x in soup.find_all('a') if type(x.get('data-download-type')) == str and (
                x.get('data-download-type').lower() == 'article pdf')]

    if len(possibleLinks) > 0:
        print("** fetching re##print using the 'NEJM' finder...")
        pdfUrl = getMainUrl(req.url) + possibleLinks[0].get('href')
        return pdfUrl

    return None



def pubmed_central_v1(req, soup, headers):
    print("====================================check 9================================")

    possibleLinks = soup.find_all('a', re.compile('pdf'))

    possibleLinks = [x for x in possibleLinks if 'epdf' not in x.get(
        'title').lower()]  # this allows the pubmed_central finder to also work for wiley

    if len(possibleLinks) > 0:
        print("** fetching re##print using the 'pubmed central' finder...")
        pdfUrl = getMainUrl(req.url) + possibleLinks[0].get('href')
        return pdfUrl

    return None


def pubmed_central_v2(req, soup, headers):
    print("====================================check 8================================")

    possibleLinks = soup.find_all('a', attrs={'href': re.compile('/pmc/articles')})

    if len(possibleLinks) > 0:
        print("** fetching re##print using the 'pubmed central' finder...")
        pdfUrl = "https://www.ncbi.nlm.nih.gov/{}".format(possibleLinks[0].get('href'))
        return pdfUrl

    return None


def science_direct(req, soup, headers):
    print("====================================check 7================================")

    newUri = urllib.parse.unquote(soup.find_all('input')[0].get('value'))
    req = requests.get(newUri, allow_redirects=True, headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')

    possibleLinks = soup.find_all('meta', attrs={'name': 'citation_pdf_url'})

    if len(possibleLinks) > 0:
        ##print("** fetching re##print using the 'science_direct' finder...")
        req = requests.get(possibleLinks[0].get('content'), headers=headers)
        soup = BeautifulSoup(req.content, 'lxml')
        pdfUrl = soup.find_all('a')[0].get('href')
        return pdfUrl
    return None

def uchicagoPress(req, soup, headers):
    print("====================================check 6================================")

    possibleLinks = [x for x in soup.find_all('a') if
                     type(x.get('href')) == str and 'pdf' in x.get('href') and '.edu/doi/' in x.get('href')]
    if len(possibleLinks) > 0:
        ##print("** fetching re##print using the 'uchicagoPress' finder...")
        pdfUrl = getMainUrl(req.url) + possibleLinks[0].get('href')
        return pdfUrl

    return None




finders = [
    'genericCitationLabelled',
    'pubmed_central_v2',
    'acsPublications',
    'uchicagoPress',
    'nejm',
    'futureMedicine',
    'science_direct',
    'direct_pdf_link',
]


headers = requests.utils.default_headers()
headers[
    'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'


if args['pmids'] != '%#$':
    pmids = args['pmids'].split(",")
    names = pmids
    print("====================================check 1================================")
else:
    print("====================================check 2================================")

    pmids = [line.strip().split() for line in open(args['pmf'])]
    if len(pmids[0]) == 1:
        print("====================================check 3================================")

        pmids = [x[0] for x in pmids]
        names = pmids
    else:
        ##print("====================================check 4================================")

        names = [x[1] for x in pmids]
        pmids = [x[0] for x in pmids]

with open(args['errors'], 'w+') as errorPmids:
    print("====================================check 5================================")

    for pmid, name in zip(pmids, names):
        print("Trying to fetch pmid {0}".format(pmid))
        retriesSoFar = 0
        while retriesSoFar < args['maxRetries']:
            ##print(pmid)
            ##print(finders)
            ##print(name)
            ##print(headers)
            ##print(errorPmids)
            try:
                soup = fetch(pmid, finders, name, headers, errorPmids)
                retriesSoFar = args['maxRetries']
            except requests.ConnectionError as e:
                if '104' in str(e) or 'BadStatusLine' in str(e):
                    retriesSoFar += 1
                    if retriesSoFar < args['maxRetries']:
                        print("** fetching of re##print {0} failed from error {1}, retrying".format(pmid, e))
                    else:
                        print("** fetching of re##print {0} failed from error {1}".format(pmid, e))
                        errorPmids.write("{}\t{}\n".format(pmid, name))
                else:
                    print("** fetching of re##print {0} failed from error {1}".format(pmid, e))
                    retriesSoFar = args['maxRetries']
                    errorPmids.write("{}\t{}\n".format(pmid, name))
            except Exception as e:
                print("** fetching of re##print {0} failed from error {1}".format(pmid, e))
                retriesSoFar = args['maxRetries']
                errorPmids.write("{}\t{}\n".format(pmid, name))


