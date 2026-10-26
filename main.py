import requests
import urllib
import os
import csv
import argparse
import sys
import shutil
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Default directories
INPUT_DIR = os.getenv("INPUT_DIR", "input")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
TIFF_NETWORK_PATH = os.getenv("TIFF_NETWORK_PATH", "")
BASE_URL = os.getenv("BASE_URL", "")
TEMPLATE = os.getenv("TEMPLATE", "")
PLACEHOLDER = os.getenv("PLACEHOLDER", "{sku}")

def ensure_directories():
  """Create input and output directories if they don't exist."""
  Path(INPUT_DIR).mkdir(exist_ok=True)
  Path(OUTPUT_DIR).mkdir(exist_ok=True)

def get_timestamped_output_dir(base_output_dir=OUTPUT_DIR):
  """Create and return a timestamped output directory with thumb and tif subdirectories."""
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  timestamped_dir = os.path.join(base_output_dir, timestamp)
  Path(timestamped_dir).mkdir(parents=True, exist_ok=True)
  
  # Create subdirectories for thumb and tif
  thumb_dir = os.path.join(timestamped_dir, "thumb")
  tif_dir = os.path.join(timestamped_dir, "tif")
  Path(thumb_dir).mkdir(exist_ok=True)
  Path(tif_dir).mkdir(exist_ok=True)
  
  return timestamped_dir, thumb_dir, tif_dir

def generate_urls_from_csv(csv_file, base_url, template, placeholder="{sku}"):
  """Generate URLs from CSV file using template and placeholder substitution."""
  urls = []
  skus = []
  
  # Check if CSV path exists as-is or in input directory
  csv_path = csv_file
  if not os.path.exists(csv_path) and os.path.exists(os.path.join(INPUT_DIR, csv_file)):
    csv_path = os.path.join(INPUT_DIR, csv_file)
  
  try:
    with open(csv_path, 'r') as f:
      reader = csv.DictReader(f)
      for row in reader:
        if not row:
          continue
        # Get the value to substitute (default to first column if specific key not found)
        value = row.get(placeholder.strip('{}'), next(iter(row.values())))
        
        # Build URL by replacing placeholder in template
        url = template.replace(placeholder, value)
        if not url.startswith('http'):
          url = base_url.rstrip('/') + '/' + url.lstrip('/')
        urls.append(url)
        skus.append(value)
    
    print(f"[OK] Generated {len(urls)} URLs from {csv_path}")
    return urls, skus
    
  except FileNotFoundError:
    print(f"[ERROR] CSV file '{csv_file}' not found.")
    print(f"  Searched: {csv_file}")
    print(f"  Also searched: {os.path.join(INPUT_DIR, csv_file)}")
    sys.exit(1)
  except Exception as e:
    print(f"[ERROR] Error reading CSV file: {e}")
    sys.exit(1)

def download_url(file_url, output_dir=OUTPUT_DIR):
  """Download a file from URL and save to output directory."""
  print(f"downloading: {file_url}")
  try:
    # Extract filename from URL
    # if url is www.test.com/abc/xyz/filename.jpg, the file name will be filename.jpg
    file_name_start_pos = file_url.rfind("/") + 1
    file_name = file_url[file_name_start_pos:]
    
    # Build full output path
    output_path = os.path.join(output_dir, file_name)
    
    # Skip if file already exists
    if os.path.exists(output_path):
      print(f"  {file_name} already exists, skipping...")
      return
   
    # Add User-Agent header to avoid 403 blocking
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    r = requests.get(file_url, stream=True, timeout=30, headers=headers)
    r.raise_for_status()  # Raise an exception for bad status codes
    
    with open(output_path, 'wb') as f:
      for chunk in r.iter_content(chunk_size=8192):
        if chunk:  # filter out keep-alive chunks
          f.write(chunk)
    
    print(f"  [OK] Successfully downloaded {file_name}")
    
  except requests.exceptions.RequestException as e:
    print(f"  [ERROR] Error downloading {file_url}: {e}")
  except IOError as e:
    print(f"  [ERROR] Error writing file {file_name}: {e}")
  except Exception as e:
    print(f"  [ERROR] Unexpected error: {e}")

def copy_tiff_file(sku, output_dir):
  """Copy TIFF file from network location to output directory."""
  tiff_filename = f"{sku}.tif"
  if not TIFF_NETWORK_PATH:
    raise RuntimeError("TIFF_NETWORK_PATH is not set. Add it to your .env file.")
  source_path = os.path.join(TIFF_NETWORK_PATH, tiff_filename)
  output_path = os.path.join(output_dir, tiff_filename)
  
  print(f"  copying TIFF: {tiff_filename} from {TIFF_NETWORK_PATH}")
  
  try:
    # Check if source file exists
    if not os.path.exists(source_path):
      print(f"    [ERROR] TIFF not found: {source_path}")
      return False
    
    # Skip if file already exists in output
    if os.path.exists(output_path):
      print(f"    {tiff_filename} already exists, skipping...")
      return False
    
    # Copy file
    shutil.copy2(source_path, output_path)
    print(f"    [OK] Successfully copied {tiff_filename}")
    return True
    
  except PermissionError:
    print(f"    [ERROR] Permission denied: Cannot access {source_path}")
    return False
  except IOError as e:
    print(f"    [ERROR] Error copying file: {e}")
    return False
  except Exception as e:
    print(f"    [ERROR] Unexpected error: {e}")
    return False


 
def main():
  parser = argparse.ArgumentParser(
    description="Bulk file downloader - Download files from URLs using CSV source",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  # Simple: Uses BASE_URL and TEMPLATE from .env file
  python main.py --csv input.csv --tif
  
  # Override .env settings with command-line arguments
  python main.py --csv items.csv --base-url https://example.com/ --template "images/{productid}.png" --placeholder "{productid}"
  
  # Using files.txt (default)
  python main.py
  
  # Custom output folder with timestamps disabled
  python main.py --csv input.csv --output assets --no-timestamp --tif
  
  # Edit .env file to set default URL and template for all runs:
  BASE_URL=https://www.4sgm.com/assets/Image/Product/thumb/
  TEMPLATE={sku}.jpg
"""
  )
  
  parser.add_argument(
    '--csv',
    default=None,
    help='CSV file in input/ directory or explicit path (default: uses files.txt if exists)'
  )
  parser.add_argument(
    '--base-url',
    default=None,
    help='Base URL for file downloads (overrides .env BASE_URL)'
  )
  parser.add_argument(
    '--template',
    default=None,
    help='URL template with placeholder (overrides .env TEMPLATE). Example: "{sku}.jpg"'
  )
  parser.add_argument(
    '--placeholder',
    default=None,
    help='Placeholder name (overrides .env PLACEHOLDER, default: {sku})'
  )
  parser.add_argument(
    '--output',
    default=OUTPUT_DIR,
    help='Output directory for downloaded files (default: output/)'
  )
  parser.add_argument(
    '--no-timestamp',
    action='store_true',
    help='Save files directly to output folder without timestamped subdirectory'
  )
  parser.add_argument(
    '--tif',
    action='store_true',
    help=f'Also copy master TIFF files from network location: {TIFF_NETWORK_PATH}'
  )
  
  args = parser.parse_args()
  
  # Ensure directories exist
  ensure_directories()
  
  url_list = []
  sku_list = []
  output_dir = args.output
  thumb_dir = None
  tif_dir = None
  
  # Create custom output directory if specified
  Path(args.output).mkdir(parents=True, exist_ok=True)
  
  # Get base URL and template: prefer command line args, fallback to .env
  base_url = args.base_url or BASE_URL
  template = args.template or TEMPLATE
  placeholder = args.placeholder or PLACEHOLDER
  
  # Option 1: Use CSV + template
  if args.csv and template:
    url_list, sku_list = generate_urls_from_csv(args.csv, base_url, template, placeholder)
    print(f"[OK] Generated {len(url_list)} URLs from {args.csv}")
    
    # Create timestamped subdirectory unless disabled
    if not args.no_timestamp:
      output_dir, thumb_dir, tif_dir = get_timestamped_output_dir(args.output)
    else:
      # Create thumb and tif subdirectories without timestamp
      thumb_dir = os.path.join(args.output, "thumb")
      tif_dir = os.path.join(args.output, "tif")
      Path(thumb_dir).mkdir(parents=True, exist_ok=True)
      Path(tif_dir).mkdir(parents=True, exist_ok=True)
    
    print(f"[OK] Output directory: {output_dir}\n")
  
  # Option 2: Use files.txt (fallback/default)
  elif not args.csv:
    try:
      with open('files.txt', 'r') as urls:
        url_list = [url.strip() for url in urls.readlines() if url.strip()]
      print(f"[OK] Found {len(url_list)} URLs in files.txt")
      
      # Create timestamped subdirectory unless disabled
      if not args.no_timestamp:
        output_dir, thumb_dir, tif_dir = get_timestamped_output_dir(args.output)
      else:
        # Create thumb and tif subdirectories without timestamp
        thumb_dir = os.path.join(args.output, "thumb")
        tif_dir = os.path.join(args.output, "tif")
        Path(thumb_dir).mkdir(parents=True, exist_ok=True)
        Path(tif_dir).mkdir(parents=True, exist_ok=True)
      
      print(f"[OK] Output directory: {output_dir}\n")
    except FileNotFoundError:
      print("[ERROR] Error: files.txt not found.")
      print("\nUsage with CSV:")
      parser.print_help()
      sys.exit(1)
  
  # Option 3: CSV provided but no template
  else:
    print("[ERROR] Error: --csv requires --template (from .env or --template argument)")
    parser.print_help()
    sys.exit(1)
  
  # Download all URLs
  if url_list:
    print(f"Starting download of {len(url_list)} files...\n")
    tiff_count = 0
    for i, url in enumerate(url_list, 1):
      print(f"[{i}/{len(url_list)}]", end=" ")
      download_url(url, thumb_dir)
      
      # Copy TIFF if enabled and SKU is available
      if args.tif and i <= len(sku_list):
        sku = sku_list[i - 1]
        if copy_tiff_file(sku, tif_dir):
          tiff_count += 1
    
    print(f"\n[OK] Completed processing {len(url_list)} files.")
    if args.tif:
      print(f"[OK] Copied {tiff_count} TIFF files from network location")
    print(f"[OK] Files saved to: {output_dir}")
  else:
    print("[ERROR] No URLs to download.")
    sys.exit(1)

if __name__ == "__main__":
  main()