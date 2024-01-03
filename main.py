TOKEN = 'MTE4NjkwMTAyNTgzNjI0OTEwOQ.G8pG5c.hacA4tfvBOCuY3zqs5apC3XeZnh5GrxdJOfD8o'
BATCH_SIZE = 5
import os
import discord
import time
from tqdm import tqdm
import json
# later add only heic
CHANNEL_ID = 1191826085248258170  # Replace with your Discord channel ID
MAIN_IMAGE_FOLDER = r'C:\Users\suhru\OneDrive\Pictures\Camera Roll'  # Replace with the path to your image folder
JSON_FILE = "saved3.json"
import os
import discord
import time
from tqdm import tqdm
import asyncio
MAX_IMAGE_SIZE_MB = 24
intents = discord.Intents.default()
intents.messages = True  # Required for the on_message event
file_formats = ['.heic', '.jpeg', '.jpg','.png','.bmp','.dng','.cr3']
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user.name}')
    try:
        await upload_images()
        print("Completed")
    except Exception as e:
        print(e)

def is_file_uploadable(file_path,size_limit = 25 * 1000 * 1000):
    return os.path.getsize(file_path) <= size_limit
async def upload_images():
    channel = client.get_channel(CHANNEL_ID)
    for root, _, files in os.walk(MAIN_IMAGE_FOLDER):
        image_files = [filename for filename in files if any([filename.endswith(file_type) for file_type in file_formats ]) and is_file_uploadable(os.path.join(root, filename)) and not(is_uploaded(os.path.join(root, filename), sha_check=True))]
        if not image_files:
            continue
        folder_name = os.path.basename(root)

        with tqdm(total=len(image_files), desc=f'Uploading Images from {folder_name}', unit='image') as pbar:
            for i in range(0,len(image_files),BATCH_SIZE):
                # filename = image_files[i]
                # file_path = os.path.join(root, filename)
                file_path_in_batch = []
                discord_file_in_batch = []
                file_pointer_in_batch = []
                for filename in image_files[i:i+BATCH_SIZE]:
                    file_path = os.path.join(root,filename)
                    file_path_in_batch.append(file_path)
                    file_pointer = open(file_path,'rb')
                    file_pointer_in_batch.append(file_pointer)
                    discord_file_in_batch.append(discord.File(file_pointer_in_batch[-1]))
                retry_count = 3
                while retry_count > 0:
                    try:
                        await channel.send(files=discord_file_in_batch)
                        for file_path in file_path_in_batch:
                            mark_as_completed(file_path)
                        time.sleep(0.2)  # Wait for one second before uploading the next image
                        pbar.update(len(file_path_in_batch))
                        break  # Break out of the retry loop if upload succeeds
                    except discord.HTTPException as e:
                        for file_path in file_path_in_batch:
                            print(file_path,os.path.getsize(file_path)/(1000 * 1000))
                        print(f'Error uploading batch: {e}')
                        retry_count -= 1
                        time.sleep(2)  # Wait for two seconds before retrying
                        continue
            for fp in file_pointer_in_batch:
                fp.close()
import hashlib
import pickle
class FileWithSHA256:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sha256_hash = FileWithSHA256.calculate_sha256(self.file_path)
    @staticmethod
    def calculate_sha256(file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as file:
            # Read the file in chunks of 4K
            for byte_block in iter(lambda: file.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    def __lt__(self, other):
        return self.sha256_hash < other.sha256_hash
class FileDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if "file_path" in dct and "sha256_hash" in dct:
            return FileWithSHA256(dct["file_path"],dct["sha256_hash"])
        return dct
class FileEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FileWithSHA256):
            return {"file_path": obj.file_path, "sha256_hash": obj.sha256_hash}
        return super().default(obj)
def mark_as_completed(file_path):
    file_exists = True
    decoded_data = []
    try:
        with open(JSON_FILE,'rb') as f:
            decoded_data = pickle.load(f)
    except:
        decoded_data = []

    with open(JSON_FILE,'wb') as f:
        decoded_data.append(FileWithSHA256(file_path))
        pickle.dump(decoded_data,f)

def is_uploaded(file_path,sha_check = True):
    try:
        open(JSON_FILE,'rb')
    except FileNotFoundError:
        return False
    with open(JSON_FILE, 'rb') as f:
        decoded_data = pickle.load(f)
        decoded_data_hash = set([file.sha256_hash for file in decoded_data])
        return FileWithSHA256.calculate_sha256(file_path) in decoded_data_hash

if __name__ == '__main__':
    asyncio.run(client.start(TOKEN))
