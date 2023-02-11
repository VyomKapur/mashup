from pytube import YouTube
from moviepy.editor import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from pydub import AudioSegment
import sys
import time
from selenium.webdriver.common.keys import Keys


sys.path.append('/path/to/ffmpeg')

class Mashup:
    def __init__(self, artist, videos):
        self.links = []
        self.artist = artist
        self.videos = videos
        self.url = "https://www.youtube.com/results?search_query="+"+".join(self.artist.split(" "))+"+latest+songs+lyrics"

    def scrape_links(self):
        options = Options()
        options.add_argument("headless")
        driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")
        driver.get(self.url)
        links = []
        while len(links) <= self.videos:
            listings = driver.find_elements(By.ID, "video-title")
            for l in listings:
                if l.get_attribute("href"):
                    links.append(l.get_attribute("href"))
            height = driver.execute_script("return document.body.scrollHeight")
            time.sleep(0.5)
            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
            if int(height)==0:
                break
        return links
    
    def download(self,links):
        audios = []
        i = 0
        for link in links:
            if(self.videos <= 0):
                break
            yt = YouTube(link)
            yt.streams.filter(only_audio=True).first().download()
            os.rename(yt.streams.first().default_filename.split(".")[0]+".mp4", f"{i}.mp3")
            audios.append(f"{i}.mp3")
            self.videos -= 1
            i+=1
        return audios

    def mash(self, audios, duration, output_filename):
        for audio in audios:
            print(audio)
            clip = AudioSegment.from_file(audio, format="mp4")
            new_clip = clip[:duration*1000]
            new_clip.export(audio, format='mp4')
        print("done")
        final_audio = ""
        for audio in audios:
            print(audio)
            sound = AudioSegment.from_file(audio, format="mp4")
            if final_audio == "":
                final_audio = sound
            else:
                final_audio += sound
        final_audio.export(output_filename, format="mp4")
        return final_audio


if __name__ == "__main__":
    artist = sys.argv[1]
    duration = sys.argv[3]
    videos = sys.argv[2]
    output_filename = sys.argv[4]

    videos = int(videos)
    duration = int(duration)
    mash_up = mashup(artist, videos)
    links = mash_up.scrape_links()
    print(links)
    audios = mash_up.download(links)
    mash_up.mash(audios, duration, output_filename)
