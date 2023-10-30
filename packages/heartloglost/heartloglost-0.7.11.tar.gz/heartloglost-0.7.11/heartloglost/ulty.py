import os
import asyncio
import math
import re

async def progress(current, total):
    prog = "Progress: " + f"{current * 100 / total:.1f}%"
    print(f"{current * 100 / total:.1f}%")
    return prog

# Function get size
def get_file_size(file_path):
    size_bytes = os.path.getsize(file_path)
    size = humanbytes(size_bytes)
    print(size)
    return size

def humanbytes(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def list_files(directory_path):
    try:
        # Get a list of all files in the specified directory
        files = os.listdir(directory_path)

        # Print the names of all files
        for file_name in files:
            print(file_name)
    except OSError as e:
        print(f"Error: {e}")

# Replace 'directory_path' with the path to the directory you want to list files from
# directory_path = "/content/torr/Wednesday.S01.COMPLETE.720p.NF.WEBRip.x264-GalaxyTV[TGx]"
# list_files(directory_path)


def youtube_url_id(url):
    regex = r"^((https?://(?:www\.)?(?:m\.)?youtube\.com))/((?:oembed\?url=https?%3A//(?:www\.)youtube.com/watch\?(?:v%3D)(?P<video_id_1>[\w\-]{10,20})&format=json)|(?:attribution_link\?a=.*watch(?:%3Fv%3D|%3Fv%3D)(?P<video_id_2>[\w\-]{10,20}))(?:%26feature.*))|(https?:)?(\/\/)?((www\.|m\.)?youtube(-nocookie)?\.com\/((watch)?\?(app=desktop&)?(feature=\w*&)?v=|embed\/|v\/|e\/)|youtu\.be\/)(?P<video_id_3>[\w\-]{10,20})"
    match = re.match(regex, url, re.IGNORECASE)
    if match:
        return (
            match.group("video_id_1")
            or match.group("video_id_2")
            or match.group("video_id_3")
        )
    else:
        return None
# url = "https://youtube.com/watch?v=yZv2daTWRZU&feature=em-uploademail"
# get_by_url(url) >> yZv2daTWRZU