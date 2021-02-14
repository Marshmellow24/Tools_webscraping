# encoding: utf-8
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

data=[]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")

with Chrome(executable_path=r'C:\Downloads\chrome\chromedriver.exe', options = chrome_options) as driver:
    wait = WebDriverWait(driver,12)
    driver.get("https://www.youtube.com/watch?v=tWosjaKmlh0")
    time.sleep(10)
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
    time.sleep(10)
    for item in range(10):
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(3)
    
    title = driver.find_element_by_tag_name("h1").text
        
    for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content-text"))):
        data.append(comment.text)
        
df = pd.DataFrame(data, columns=['comment'])
#df.style.set_properties(**{'text-align': 'left'})
#df = df.stack().str.lstrip().unstack()

#with pd.option_context('display.max_colwidth', 3):
#    print (df)

title = re.sub(r"[ -:!?*/\"<>|]", "_", title)
title = re.sub(r"_+", "_", title)
title = title.lower()
print("C:\\Texte\\UNI\\Master WiInfo\\Seminararbeit UM\\youtube\\comments\\" + title + r".txt")
print(df.to_string(index = False, justify="start"))
with open("C:\\Texte\\UNI\\Master WiInfo\\Seminararbeit UM\\youtube\\comments\\"
          + title + r".txt", "w", encoding = "utf-8") as f:
    f.write(df.to_string(header = False, index = False, justify = "initial"))
    
    