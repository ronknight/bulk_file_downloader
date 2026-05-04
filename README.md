<p><a target="_blank" href="https://app.eraser.io/workspace/aS4lSWNHoIQeVO45UQSF" id="edit-in-eraser-github-link"><img alt="Edit in Eraser" src="https://firebasestorage.googleapis.com/v0/b/second-petal-295822.appspot.com/o/images%2Fgithub%2FOpen%20in%20Eraser.svg?alt=media&amp;token=968381c8-a7e7-472a-8ed6-4a6626da5501"></a></p>

<h1 align="center"><a href="https://github.com/ronknight/bulk_file_downloader">Bulk File Downloader</a></h1>
<h4 align="center">Robust bulk file downloader with streaming support, error handling, and progress tracking. Download images, PDFs, mp3s, and more from multiple URLs using Python 3.</h4>

<p align="center">
<a href="https://twitter.com/PinoyITSolution"><img src="https://img.shields.io/twitter/follow/PinoyITSolution?style=social"></a>
<a href="https://github.com/ronknight?tab=followers"><img src="https://img.shields.io/github/followers/ronknight?style=social"></a>
<a href="https://youtube.com/@PinoyITSolution"><img src="https://img.shields.io/youtube/channel/subscribers/UCeoETAlg3skyMcQPqr97omg"></a>
<a href="https://github.com/ronknight/bulk_file_downloader/issues"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
<a href="https://github.com/ronknight/bulk_file_downloader/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
<a href="#"><img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg"></a>
<a href="https://github.com/ronknight"><img src="https://img.shields.io/badge/Made%20with%20%F0%9F%A4%8D%20by%20-%20Ronknight%20-%20red"></a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#diagrams">Diagrams</a> •
</p>

---

## Features

✅ **Robust Streaming Downloads** - Efficient memory usage with chunked streaming  
✅ **Comprehensive Error Handling** - Network timeouts, HTTP errors, and file I/O protection  
✅ **Progress Tracking** - Real-time download progress with status indicators  
✅ **Duplicate File Detection** - Automatically skips existing files  
✅ **Timeout Protection** - 30-second timeout prevents hanging downloads  
✅ **User-Friendly Output** - Clear success (✓) and error (✗) indicators  
✅ **Bulk Processing** - Process hundreds of URLs from a simple text file  

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ronknight/bulk_file_downloader.git
cd bulk_file_downloader
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. **Prepare your URLs**: Create a `files.txt` file with one URL per line:
```
https://example.com/image1.jpg
https://example.com/document.pdf
https://example.com/audio.mp3
```

2. **Run the downloader**:
```bash
python main.py
```

3. **Example Output**:
```
Found 8 URLs to download...

[1/8] downloading: https://www.4sgm.com/assets/Image/Product/thumb/30067.jpg
  ✓ Successfully downloaded 30067.jpg

[2/8] downloading: https://www.4sgm.com/assets/Image/Product/thumb/30061.jpg
  30061.jpg already exists, skipping...

✓ Completed processing 8 URLs.
```

### Supported File Types
- **Images**: JPG, PNG, GIF, BMP, WEBP, SVG
- **Documents**: PDF, DOC, DOCX, TXT, RTF  
- **Audio**: MP3, WAV, FLAC, AAC
- **Video**: MP4, AVI, MOV, MKV
- **Archives**: ZIP, RAR, 7Z, TAR
- **Any other file type with direct download links**
# Screenshots

## RUN PROGRAM
![Run Program](https://github.com/ronknight/bulk_file_downloader/blob/master/assets/run-program.png "")

## BEFORE DOWNLOAD
![Before Download](https://github.com/ronknight/bulk_file_downloader/blob/master/assets/before-download.png "")

## AFTER DOWNLOAD
![After Download](https://github.com/ronknight/bulk_file_downloader/blob/master/assets/after-download.png "")

## Error Handling

The downloader includes robust error handling for common issues:

- **Network Errors**: Automatic timeout protection (30 seconds)
- **HTTP Errors**: Proper handling of 404, 403, and other HTTP status codes
- **File Errors**: Protection against permission issues and disk space problems
- **Invalid URLs**: Graceful handling of malformed URLs
- **Missing Files**: Clear error message when `files.txt` is not found

### Common Issues

**Files not downloading?**
- Check that URLs in `files.txt` are valid and accessible
- Ensure you have write permissions in the directory
- Verify your internet connection

**Timeout errors?**
- Some servers may be slow; the 30-second timeout should handle most cases
- Try downloading fewer files at once if experiencing consistent timeouts

**Permission errors?**
- Run the terminal as administrator (Windows) or use `sudo` (Linux/Mac)
- Check that the destination directory is writable




<!-- eraser-additional-content -->
## Diagrams
<!-- eraser-additional-files -->
<a href="/README-Bulk Download Process-1.eraserdiagram" data-element-id="JrJiABes2KbcklXfSUIFk"><img src="/.eraser/aS4lSWNHoIQeVO45UQSF___3Jivg2tjMecMlrHwbIVIBR8f7U03___---diagram----5b7e579351815fcb6ff79d07b3a6c10f-Bulk-Download-Process.png" alt="" data-element-id="JrJiABes2KbcklXfSUIFk" /></a>
<!-- end-eraser-additional-files -->
<!-- end-eraser-additional-content -->
<!--- Eraser file: https://app.eraser.io/workspace/aS4lSWNHoIQeVO45UQSF --->