import asyncio
import grpc
from grpc import aio
import zipfile
from . import zip_service_pb2
from . import zip_service_pb2_grpc
import logging

class ZipClient:
    def __init__(self, ip, zip_progress_callback, download_progress_callback):
        self.stub = None
        self.zip_progress_callback = zip_progress_callback
        self.download_progress_callback = download_progress_callback
        self.ip = ip

    async def start(self, directory):
        # Create gRPC channel and stub
        channel = aio.insecure_channel(f'{self.ip}:50051')
        self.stub = zip_service_pb2_grpc.ZipServiceStub(channel)

        # Call StartZip
        request = zip_service_pb2.ZipRequest(dir=directory)
        async for response in self.stub.StartZip(request):
            self.zip_progress_callback(response.progress)

        # Call DownloadZip
        downloaded_data = b''
        request = zip_service_pb2.DownloadRequest(filename='output.zip')
        async for response in self.stub.DownloadZip(request):
            if response.data:
                downloaded_data += response.data
                progress = response.sent_size / response.total_size
                self.download_progress_callback(progress)
                
        # Save the downloaded zip file
        with open('downloaded.zip', 'wb') as f:
            f.write(downloaded_data)

        await channel.close()

    def start_sync(self, directory):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.start(directory))
        finally:
            loop.close()
            asyncio.set_event_loop(None)


def zip_progress_update(progress):
    print('Zip Progress: {:.2f} %'.format(progress * 100))

def download_progress_update(progress):
    print('Download Progress: {:.2f} %'.format(progress * 100))


# User code:
if __name__ == '__main__':
    logging.basicConfig()
    client = ZipClient(zip_progress_update, download_progress_update)
    client.start_sync('/Users/luzhipeng/Desktop/Images/图片')
