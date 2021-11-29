import requests
import json
import cv2
import pytz
import time
import re
import os
import subprocess
import sys
import psutil
import signal
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from geopy.geocoders import Nominatim
from subprocess import Popen, PIPE
import urllib.request


class Downloader:
    def __init__(self, file_name):
        self.procs = []
        self.output_dir = "scraped_data/Maryland/"
        with open(file_name, "r") as file:
            self.config = json.load(file)
        self.urls = [self.config["features"][i]["attributes"].get(
            "CCTVPublicURL") for i in range(len(self.config["features"]))]
        self.dirs = [self.config["features"][i]["attributes"].get(
            "location") for i in range(len(self.config["features"]))]
        for i in range(len(self.dirs)):
            self.dirs[i] = self.dirs[i].replace(" ", "_")
            self.dirs[i] = self.dirs[i].replace("|", "")
            path = os.path.join(self.output_dir, self.dirs[i])
            self.dirs[i] = path
            if not os.path.exists(path):
                os.makedirs(path)

        self.lats = [str(self.config["features"][i]["attributes"].get(
            "Latitude")) for i in range(len(self.config["features"]))]
        self.longs = [str(self.config["features"][i]["attributes"].get(
            "Longitude")) for i in range(len(self.config["features"]))]

    def download_image(self, cam_url, file_path, lat, longitude):
        """[summary]
        Args:
            cam_url (string): CCTV Link
            file_path (string): File path of folder
            lat (string): Latitude of camera
            longitude (string): Longitude of camera
        """

        # get metadata information for JSON file

        geolocator = Nominatim(user_agent="geoapiExercises")
        api_key = "5d5ca308df10a667a3d584ced88a827f"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"

        # reverse geocoding lat long from camera link to county

        location = geolocator.reverse(lat + "," + longitude)
        address = location.raw['address']
        county = address.get('county', '')

        # getting time and date

        tz_EST = pytz.timezone('America/New_York')
        datetime_EST = datetime.now(tz_EST)
        start_time = datetime_EST.strftime("%H-%M-%S")

        end_time = datetime.now(tz_EST) + timedelta(hours=1)
        end_time = end_time.strftime("%H-%M-%S")

        today = date.today()
        today = today.strftime("%m-%d-%y")

        # file name

        image_name = today + "_" + start_time

        # getting weather report

        url = base_url + "q=" + county + "&appid=" + api_key
        response = requests.get(url)
        data = response.json()
        main = data['main']
        temperature = main['temp']
        report = data['weather']
        description = report[0]['description']

        # creating JSON file

        metadata = {
            "CCTVPublicURL": cam_url,
            "County": county,
            "Latitude": lat,
            "Longitude": longitude,
            "Date (MM-DD-YY)": today,
            "Video Start Time (HH: MM: SS)": start_time,
            "Video End Time (HH: MM: SS)": end_time,
            "Temperature (K)": temperature,
            "Weather Description": description
        }

        jsonString = json.dumps(metadata, indent=4)
        jsonFile = open(file_path + "/" + image_name + ".json", "w")
        jsonFile.write(jsonString)

        #####################################################################

        # image download code

        page = requests.get(cam_url)
        data = page.text
        soup = BeautifulSoup(data, 'html.parser')
        script = str(soup.find_all('script')[2])

        urls = re.findall(r'\'(.+?)\'', script)
        download_link = urls[1]

        proc = subprocess.Popen(
            f"ffmpeg -i \"{download_link}\" -codec copy -t 01:00:00 {file_path}/{image_name}.mp4")

        return proc

    def run(self):
        """[summary]
        Run download image function with all paramters
        """

        for i in range(len(self.urls)):
            proc = self.download_image(
                self.urls[i], self.dirs[i], self.lats[i], self.longs[i])
            self.procs.append(proc)
            print(proc)
        for i in range(5):
            time.sleep(3600)
            for proc in self.procs:
                proc.terminate()
                proc.start()
        for proc in self.procs:
            proc.terminate()

    def delete(self):
        """[summary]
        delete empty folders after run function is called
        """

        for dirpath, dirnames, filenames in os.walk(self.output_dir, topdown=False):
            if not dirnames and not filenames:
                os.rmdir(dirpath)


if __name__ == "__main__":
    d = Downloader("maryland.json")
    d.run()
    d.delete()
