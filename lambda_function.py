from selenium import webdriver
import boto3
from datetime import datetime
import os
import glob

CAPTURE_FILE="screenshot.png"
ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'


def screen_shot(driver, file_name=CAPTURE_FILE):
    w = driver.execute_script('return document.body.scrollWidth')
    h = driver.execute_script('return document.body.scrollHeight')
    driver.set_window_size(w, h)
    # driver.save_screenshot(file_name)
    print("exec screenshot")
    driver.save_screenshot('/var/task/screenshot.png')
    driver.save_screenshot('/screen.png')

def lambda_handler(event, context):
    options = webdriver.ChromeOptions()

    # のちほどダウンロードするバイナリを指定
    options.binary_location = "./bin/headless-chromium"

    # headlessで動かすために必要なオプション
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--homedir=/tmp")

    driver = webdriver.Chrome(
        "./bin/chromedriver",
        chrome_options=options)
    driver.get(ENDPOINT_URL)
    title = driver.title

    screen_shot(driver)

    driver.close()
    print("hogehoge")
    print(os.getcwd())
    print(glob.glob('/var/task/*'))

    s3 = boto3.resource('s3')
    bucket = 'aqours-4th-vote'    # ⑤バケット名を指定
    # key = 'test_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.txt'  # ⑥オブジェクトのキー情報を指定
    # file_contents = 'Lambda test'  # ⑦ファイルの内容
    
    # obj = s3.Object(bucket,key)     # ⑧バケット名とパスを指定
    # obj.put( Body=file_contents )
    s3.Bucket(bucket).upload_file('/screen.png', 'screen_shot1.png')
    s3.Bucket(bucket).upload_file('/var/task/screenshot.png', 'screen_shot.png')


    return title