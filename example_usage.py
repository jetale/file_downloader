from file_downloader import downloader


dwnldr_obj = downloader.FileDownloader()
dwnld_gen = dwnldr_obj.download_and_return()
vals = next(dwnld_gen)
print(vals)
