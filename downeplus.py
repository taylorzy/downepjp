import os
from selenium import webdriver
from time import sleep

from tqdm import tqdm


def parse_m3u8(filename):
    ts_paths = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if line.endswith('.ts'):
                ts_paths.append(line)
    return ts_paths


outdir = 'ts_video'
if not os.path.exists(outdir):
    os.mkdir(outdir)

ts_paths = parse_m3u8('xxxxxxx.m3u8') # the m3u8 file name downloaded locally

view_url = 'https://live.eplus.jp/xxxxxx'    # url to watch eplus stream
ts_host_url = 'https://vod.live.eplus.jp/out/v1/xxxxxx/'  # url to download ts files


def site_login(driver:webdriver.Chrome):
    driver.get (view_url)
    driver.find_element_by_id('loginId').send_keys('userId')
    driver.find_element_by_id ('loginPassword').send_keys('password')
    driver.find_element_by_id('idPwLogin').click()

def download_ts(driver:webdriver.Chrome, ts_path):
    path = os.path.join(outdir, ts_path)
    if os.path.exists(path):
        return False
    driver.get(ts_host_url + ts_path)
    return True

def main():
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
            'download.default_directory': os.path.abspath(outdir)}  # change chrome driver default download url to outdir
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--headless')    # do not actually show the Chrome browser for testing

    driver = webdriver.Chrome(
        executable_path='/usr/local/bin/chromedriver', chrome_options=options)
    site_login(driver)

    downloading = 0
    for path in tqdm(ts_paths):
        if download_ts(driver, path):
            downloading += 1
        if downloading == 10:
            sleep(10)  # sleep to avoid server throttle
            downloading = 0

while True:
    try:
        main()
    except Exception as e:
        print(f'Exception {e} occured, restarting...')
        os.system('rm -rf *.crdownload')  # delete Chrome temp download dir
        sleep(100)
    else:
        break