import requests
import urllib

def download_url(file_url):
  print("downloading: ",file_url)
  # find "/" then assume that all the rest of the charaters after that represents the filename
  # if url is www.test.com/abc/xyz/filename.jpg, the file name will be filename.jpg
  file_name_start_pos = file_url.rfind("/") + 1
  file_name = file_url[file_name_start_pos:]
 
  r = requests.get(file_url, stream=True)
  if r.status_code == requests.codes.ok:
    with open(file_name, 'wb') as f:
      for data in r:
        f.write(data)
 
with open('files.txt', 'r') as urls:
  for url in urls.readlines():
    # go through all the URLs on the txt file separated by new line.
    # remove newline character from the URL
    url = url.rstrip("\n")
    download_url(url)