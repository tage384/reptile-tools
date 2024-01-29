import argparse
import os
import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from tqdm import tqdm




def get_m4a(base_url, count, driver, save_path):
    # 访问URL
    driver.get(base_url)
    try:
        time.sleep(5)
        driver.find_element(By.XPATH, "//*[@id='award']/main/div[1]/div[2]/div[1]/div[1]/div/div[2]/xm-player/div").click()
        time.sleep(15)
    except:
        print("Fault!")
    mian_url = ''
    for request in driver.requests:
        if request.response:
            # print(request.url)
            if "audiopay.cos.tx.xmcdn.com" in request.url:
                # print(request.url)
                mian_url = request.url
    try:
        with open(save_path + str(count) +".m4a","wb") as f:
            f.write(requests.get(mian_url).content)
    except:
        print("write failed!" , request.url)

def main(args):
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('log-level=3')

    driver = webdriver.Chrome(chrome_options=chrome_options)
    url = args.url
    start = args.start
    save_path = args.save_path
    driver.get(url)

    # 登陆操作，需要手动扫码登陆
    try:
        driver.find_element(By.XPATH, "//*[@id='rootHeader']/div/div[2]/div/div").click()
        time.sleep(10)
    except:
        print("Click Failed")

    # 获取列表页数
    pages = driver.find_elements(By.XPATH, "//*[@id='anchor_sound_list']/div[2]/div/nav/ul/li/a/span")
    page_num = int(pages[-1].text)
    tags = []
    m4as = []

    print("抓取音频链接......")
    # 遍历获取每个音频链接
    for i in tqdm(range(1, page_num+1)):
        input_box = driver.find_element(By.XPATH, "//*[@id='anchor_sound_list']/div[2]/div/nav/div/form/input")
        search_btn = driver.find_element(By.XPATH, "//*[@id='anchor_sound_list']/div[2]/div/nav/div/form/button")
        input_box.send_keys(i)
        search_btn.click()
        input_box.clear()
        time.sleep(5)
        ul = driver.find_element(By.XPATH, "//*[@id='anchor_sound_list']/div[2]/ul")
        tags = ul.find_elements(By.TAG_NAME, "li")
        # print(len(tags))
        
        j = 0
        while j < len(tags):
            tag = tags[j]
            try:
                href = tag.find_element(By.TAG_NAME,"a")
                # print(href.text, href.get_attribute('href'))
                m4as.append(href.get_attribute('href'))
                j += 1
            except:
                print("Fault!")
    print(m4as)
    print("下载 m4a 文件.....")
    for i, m4a in tqdm(enumerate(m4as)):
        if i > start - 1:
            get_m4a(m4a, i+1, driver, save_path)   
    driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='喜马拉雅网页广播剧爬取')

    parser.add_argument('--url', default="https://www.ximalaya.com/album/30816438")
    parser.add_argument('--start', default=9)
    parser.add_argument('--save_path', default='广播剧/BaiduSyncdisk/三体/santi')
    args = parser.parse_args()

    main(args)

