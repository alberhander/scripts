# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
from urllib.request import urlretrieve

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  hostname = re.search(r'[^_]+\.google\.com',filename).group()
  img_urls = []
  img_dicts = []

  logfile = open(filename, 'r')
  lines = logfile.readlines()
  logfile.close()

  for line in lines:
  	try:
  		path = re.search(r'GET\s(\/[^\s]+\.(?:ico|jpg|jpeg|png))+',line).group(1)
  		url = 'https://%s%s'%(hostname,path)
  		secondword = re.search(r'\-([^\s,-]+)\.(?:ico|jpg|jpeg|png)',url).group(1)
  		if url not in img_urls:
  			img_urls.append(url)
  			img_dict = {
  			'secondword': secondword,
  			'url': url
  			}
  			img_dicts.append(img_dict)
  	except:
  		continue

  sorted_list_dicts = sorted(img_dicts, key=lambda k: k['secondword'])
  sorted_list_urls = []
  for item in sorted_list_dicts:
  	sorted_list_urls.append(item['url'])

  return sorted_list_urls
  

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  os.system('mkdir -p %s'%dest_dir)

  img_tags = ''
  for id,url in enumerate(img_urls):
  	print('Retrieving img%s'%id)
  	try:
  		response = urlretrieve(url)
  		os.system('mv %s %s/img%s'%(response[0],dest_dir,str(id)))
  		tag = '<img src="%s/img%s">'%(dest_dir,str(id))
  		img_tags += tag
  	except:
  		continue


  index = """
    <verbatim>
      <html>
      <body>
      %s
      </body>
      </html>
      """%img_tags

  f = open('index.html','w')
  f.write(index)
  f.close()

def main():
  args = sys.argv[1:]

  if not args:
    print('usage: [--todir dir] logfile ')
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print('\n'.join(img_urls))

if __name__ == '__main__':
  main()
