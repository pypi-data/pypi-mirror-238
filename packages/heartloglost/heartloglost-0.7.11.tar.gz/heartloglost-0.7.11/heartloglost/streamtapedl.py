import PyBypass as bypasser
import time
import os
import requests
from bs4 import BeautifulSoup
from .pypdl import pypdl_download

def streamtapebye(slink):
    while True:
        bypassed_link = bypasser.bypass(slink, name="streamtape")
        if len(bypassed_link) > 50:
            return bypassed_link
        print("Incomplete URL, retrying in 2 seconds...")
        time.sleep(2)


# url = "https://streamtape.com/v/o6PrJ2B16PSJ14j/Happy_Happy_Cat_but_famous_phone_ringtones.mp4"
# print(streamtapebye(url))

def SaveTape(url, location):
    try:
        direct_url = streamtapebye(url)
        pypdl_download(direct_url, location)
        return location
    except Exception as e:
        print(e)


def tapeimg_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        og_image_tag = soup.find('meta', {'name': 'og:image'})
        if og_image_tag:
            image_url = og_image_tag['content']
            return image_url
        else:
            return None
    except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

# print(tapeimg_url("https://streamtape.com/v/o6PrJ2B16PSJ14j/"))

def SavePic(url, directory, filename):
    try:
        os.makedirs(directory, exist_ok=True)
        response = requests.get(url)
        if response.status_code == 200:
            # Save the image
            with open(os.path.join(directory, filename), 'wb') as file:
                file.write(response.content)
            print(f"Image saved successfully at {os.path.join(directory, filename)}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def SavePicAdv(url, save_dir, num_connections=10):
    try:
        pypdl_download(url, save_dir, num_connections)
    except Exception as e:
        print("e")
        

# SavePicAdv(tapeimg_url("https://streamtape.com/v/o6PrJ2B16PSJ14j/"), "/content/Savedf/HU.jpg")



# urlto = "https://wsrv.nl/?h=320&w=320&q=80&url=" + get_image_url("https://streamtape.com/v/3PpR3x4W7Qiddwk")
# SavePic(urlto, "GoogleColab", "output_imagefrf.jpg")