import asyncio
import aiohttp
import os
import tarfile


class FileDownloader:

    async def download_from_urls(self, urls: list):
        async with aiohttp.ClientSession() as session:
            # Gather all tasks while ensuring the session stays open
            all_tasks = [
                self.download_and_extract(url, session) for url in urls
            ]
            await asyncio.gather(*all_tasks)

    async def download_and_extract(self, url: str, session):
        local_filename = url.split('/')[-1]
        if self.file_exists(local_filename):
            print(f"File already exists: {local_filename} from {url}")
            return
        else:
            await self.download_single_file(url, local_filename, session)
            print(f"Downloaded: {local_filename}")
            if local_filename.endswith('.tar.bz2'):
                self.extract_tar_bz2(local_filename)

    @staticmethod
    async def download_single_file(url, local_filename, session):
        print(f"Downloading: {local_filename} from {url}")
        async with session.get(url) as response:
            response.raise_for_status()  # Raise an error for bad responses
            with open(local_filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        print("Downloaded: ", local_filename)

    @staticmethod
    def file_exists(filename):
        return os.path.isfile(filename)

    @staticmethod
    def extract_tar_bz2(filename):
        print(f"Extracting: {filename}")
        with tarfile.open(filename, 'r:bz2') as tar:
            tar.extractall()  # Extract to the current directory
        print(f"Extracted: {filename}")
