#               github.com/aemirdnr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from pydub import AudioSegment

import speech_recognition as sr
import requests
import time

chrome_options = webdriver.ChromeOptions()
#Private mode
chrome_options.add_argument("--incognito")

#Chromedriver.exe PATH
driver = webdriver.Chrome(options=chrome_options, executable_path=r"C:\Users\V OF W\Desktop\captcha-f\driver.exe")

driver.get("https://www.google.com/recaptcha/api2/demo")

time.sleep(5)

WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()

driver.switch_to.default_content()

WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='recaptcha challenge']")))
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#recaptcha-audio-button"))).click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "audio-source")))
source = driver.find_element_by_id("audio-source").get_attribute("src")

file = requests.get(source)

with open("audio.mp3", "wb") as f:
    f.write(file.content)

sound = AudioSegment.from_mp3("audio.mp3")
sound.export("audio.wav", format="wav")

r = sr.Recognizer()
audioFile = sr.AudioFile("audio.wav")

with audioFile as source:
    r.adjust_for_ambient_noise(source)
    audio = r.record(source)

print(r.recognize_google(audio))

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "audio-response")))
tbox = driver.find_element_by_id("audio-response")
tbox.send_keys(r.recognize_google(audio))

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "recaptcha-verify-button")))
driver.find_element_by_id("recaptcha-verify-button").click()
