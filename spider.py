# Crawler
# Fetch the webpage for URL provided.
# Parse all the links in page to repository
# Fetch the content of URL from repository
# Process continues for all links or
# Till maximum links defined is reached
#
# Author: Prashannth Vijayakumar
#

import re
import pycurl
import utils
from BeautifulSoup import BeautifulSoup
from StringIO      import StringIO

class Spider:
    """
    A Spider Class.

    For crawling a webpage
    """

    log        = True
    baseUrl    = ""
    repository = []
    max_links   = 100
    status     = 0
    stop       = "no"

    def __init__(self, args):
        """Initializing the spider here.
        :param args: argument with necessary details
        """
        # If there is no key named url in args throw exception
        if 'url' not in args:
            raise Exception("`url` required for spider")

        # Check for valid url
        if not self.isValidUrl(args['url']):
            raise Exception(args['url'] + ' is not a valid url.')

        self.baseUrl = args['url']

        # log definition
        if 'log' in args:
            if type(args['log']) == type(True):
                self.log = args['log']

        # max links arg
        if type(args['max_links']) == type(3):
            self.maxLinks = args['max_links']

        print "\nALL SET SPIDER GOING TO START\n"
        self.startCurl(self.baseUrl)

    def logging(self, msg):
        """For logging stuffs.
        :param msg: Message which is need to be logged
        """
        print msg
        print "*****************************"

    def startCurl(self, url):
        """Initializing the URL fetch or crawl process.
        :param url: URL to be fetched or crawled
        """

        # Stopping the progress
        # once max_links is reached
        if self.stop == 'yes':
            return

        # Logging the details
        if self.log:
            self.logging("FETCHING " + url)

        # Necessary Curl operations and conditions
        buffer = StringIO()
        headerBuffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.CONNECTTIMEOUT, 30)
        c.setopt(c.AUTOREFERER,1)
        c.setopt(c.FOLLOWLOCATION, 1)
        c.setopt(c.COOKIEFILE, '')
        c.setopt(c.TIMEOUT, 30)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        if self.log:
            self.logging("FETCHING COMPLETED FOR " + url)
        self.parsing(buffer.getvalue())

    def parsing(self, data):
        """Parsing the content using beautifulsoup
        :param data: argument with necessary details
        """

        # Stopping the progress
        # Once max_links reached
        if self.stop == 'yes':
            return

        # Logging details
        if self.log:
            self.logging("PARSING STARTED ")

        # try parsing with beautigulsoup
        try:
            soup = BeautifulSoup(data)

        # exception on parse failed
        # that is parse failed in case of binary files
        except:
            if self.log:
                self.logging("PARSING FAILED ")
            return

        # For finding the valid links and adding to repository
        for link in soup.findAll('a', attrs={'href': re.compile("^http(s)?://")}):

            # check for valid url
            if self.isValidUrl(link.get('href')):

                # append to repo if valid url
                self.repository.append(link.get('href'))
                if self.log:
                    self.logging( link.get('href') + " added to repository")

                # stop when reached max_links
                if len(self.repository) >= self.maxLinks:
                    self.stop="yes"
                    return self.repository
        if not self.status:
            self.startRecursive()

    def startRecursive(self):
        """Start recursive curl
        """

        if self.stop == 'yes':
            return
        self.status = 1
        for link in self.repository:
            self.startCurl(link)

    def isValidUrl(self, url):
        """Check for valid URL
        :param url: url to parse or fetch
        """

        # stopping the progress
        # on maximum link reached
        if self.stop == 'yes':
            return

        # regex check for URL
        regex = re.compile(
            r'^(?:http)s?://'     # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        # return true if regex matches
        # return false if not matches
        if not regex.match(url):
            return False
        else:
            return True

# input
URL = utils.sanitize_url(raw_input('Enter the url to crawl : '), '')
MAX_LINK_TO_FETCH = input('Enter the maximum number of links to crawl : ')

# execution section
spider = Spider({
    "url": URL,                      #URL to crawl
    "log": True,
    "max_links": MAX_LINK_TO_FETCH   #Depth to crawl
})
print spider.repository
print "\nTotal Links fetched Succesfully: " + str(len(spider.repository)) + "\n"
print "****   GOOD BYE. SPIDER FINISHED ****"
