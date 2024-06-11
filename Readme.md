## File Downloader Script

#### Cloning -
```
git clone https://github.com/jetale/file_downloader
```

#### Example usage -
```
from file_downloader import downloader

downloader_obj = downloader.FileDownloader()
downloader_gen = downloader_obj.download_and_return()  # This downloades the files and returns the path
first_two_files = next(downloader_gen)   # This downloads and returns the file paths for the first row

```
