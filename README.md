# Python Link Crawler

A crawler is a program that starts with a url on the web (ex: http://python.org), fetches the web-page corresponding to that url, and parses all the links on that page into a repository of links. Next, it fetches the contents of any of the url from the repository just created, parses the links from this new content into the repository and continues this process for all links in the repository until stopped or after a given number of links are fetched.

This is a simple crawler program.

## How to use:

### Clone the repository using the following command:

```
git clone https://github.com/prashannth/python-link-crawler.git
```

### Install the requirements:

```
pip install requirements.txt
```

**Note:** Please install the dependency manually even though above command fails, This is must for going ahead.

### Edit the file based on your requirement:

#### Add your URL here:

[https://github.com/prashannth/python-link-crawler/blob/master/spider.py#L176]

#### Add maximum links limit here:

[https://github.com/prashannth/python-link-crawler/blob/master/spider.py#L178]

### Execute the file:

```
python spider.py
```

Wait for sometime :) Enjoy Crawling :)
