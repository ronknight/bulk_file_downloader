import requests
import urllib
import os

def download_url(file_url):
  print(f"downloading: {file_url}")
  try:
    # find "/" then assume that all the rest of the charaters after that represents the filename
    # if url is www.test.com/abc/xyz/filename.jpg, the file name will be filename.jpg
    file_name_start_pos = file_url.rfind("/") + 1
    file_name = file_url[file_name_start_pos:]
    
    # Skip if file already exists
    if os.path.exists(file_name):
      print(f"  {file_name} already exists, skipping...")
      return
   
    r = requests.get(file_url, stream=True, timeout=30)
    r.raise_for_status()  # Raise an exception for bad status codes
    
    with open(file_name, 'wb') as f:
      for chunk in r.iter_content(chunk_size=8192):
        if chunk:  # filter out keep-alive chunks
          f.write(chunk)
    
    print(f"  ✓ Successfully downloaded {file_name}")
    
  except requests.exceptions.RequestException as e:
    print(f"  ✗ Error downloading {file_url}: {e}")
  except IOError as e:
    print(f"  ✗ Error writing file {file_name}: {e}")
  except Exception as e:
    print(f"  ✗ Unexpected error: {e}")
 
 
def main():
  try:
    with open('files.txt', 'r') as urls:
      url_list = [url.strip() for url in urls.readlines() if url.strip()]
      
    print(f"Found {len(url_list)} URLs to download...")
    
    for i, url in enumerate(url_list, 1):
      print(f"\n[{i}/{len(url_list)}]", end=" ")
      download_url(url)
      
    print(f"\n✓ Completed processing {len(url_list)} URLs.")
    
  except FileNotFoundError:
    print("✗ Error: files.txt not found. Please create a files.txt file with URLs to download.")
  except Exception as e:
    print(f"✗ Unexpected error: {e}")

if __name__ == "__main__":
  main()