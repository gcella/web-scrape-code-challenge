# Gabrielle Cella email address scraper coding challenge


import sys
import urllib2
from bs4 import BeautifulSoup
import re
from urlparse import urljoin



def find_emails_on(curr_page, emails, visited_pages, url):
	# Ensure each page is only visited once (prevents cycles/infinite recursion)
	if (curr_page in visited_pages or curr_page+'/' in visited_pages):
		return
	# Ensure page is in proper domain
	if not curr_page.startswith(url):
		return

	visited_pages.add(curr_page)
	print curr_page 

	hdr = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
	req = urllib2.Request(curr_page, headers=hdr)

	try:
		response = urllib2.urlopen(req)
		print "TYPE: " + response.info().getheader('Content-Type')
		
		# Avoid reading from non-html pages (e.g. .pdf, .exe, .mp3, etc)
		if not response.info().getheader('Content-Type').startswith('text/html'):
			return

		# Find all emails in a page's html, update email set
		page = response.read()
		curr_emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', page)
		emails.update(curr_emails)
		print set(curr_emails)

		soup = BeautifulSoup(page, "html.parser")

		# Find all absolute links to other pages
		for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
			find_emails_on(link.get('href'), emails, visited_pages, url)
		
		# Find all relative links
		for link in soup.findAll('a', href=True):
			if urljoin(curr_page, link['href']).startswith(url):
				find_emails_on(urljoin(curr_page, link['href']), emails, visited_pages, url)

	except urllib2.HTTPError as e:
	    sys.stderr.write(str(e.code))
	    sys.stderr.write(e.read()) 


def main():
	url = sys.argv[1]
	if '//' not in url:
		url = 'http://' + url
	print url
	res = urllib2.urlopen(url)
	if res.url != url:
		print "The URL you have entered redirects to: " + res.url + " Searching instead for that URL"
		url = res.url
	emails = set()
	visited_pages = set()
	find_emails_on(url, emails, visited_pages, url)

	print set(emails)


if __name__ == "__main__":
	main()

