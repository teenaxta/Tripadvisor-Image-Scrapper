from selenium import webdriver
import requests
import io
from PIL import Image
import time
from selenium.webdriver.common.by import By

import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

from webdriver_manager.chrome import ChromeDriverManager




def get_hotel_page_urls_from_main_page(place, csv_path, total_num_pages=5):
    # Get all the hotels on the first page. There are some 30 hotels, that should be sufficient for our purposes. 
    print(place)
    driver=webdriver.Chrome()
    base = "https://www.tripadvisor.com/"

    hotel_page_urls=[]

    for i in range(total_num_pages):

        url = f'https://www.tripadvisor.com/Search?q={place}&ssrc=h&o={i*30}'
        driver.get(url)
        driver.refresh()
        time.sleep(4)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page_indexes=driver.find_elements(By.CLASS_NAME,'result-title')

        # Extracting URLs from web elements
        
        for page_index in  page_indexes:
            hotel_url_subset = page_index.get_attribute('onclick').split(',')[3].split("'")[1] ##URL of hotel page is a bit different from the one we extract from element 
            hotel_page_urls.append(base + hotel_url_subset ) # This makes the URL in standard notation. eg https://www.tripadvisor.com//Hotel_Review-g295413-d308291-Reviews-Pearl_Continental_Lahore-Lahore_Punjab_Province.html
        
    df = pd.DataFrame(hotel_page_urls)
    df.to_csv(csv_path+place+'.csv', index=False)

    driver.close()
    driver.quit()

    return hotel_page_urls

def get_img_urls_from_hotel_page(hotel_page_url, image_width = 300):
    hotel_page_url = hotel_page_url[0] + '#/media' ## /4451234/?albumid=19&type=0&category=19'
    #page_driver=webdriver.Chrome(ChromeDriverManager().install())
    page_driver=webdriver.Chrome()
    page_driver.get(hotel_page_url)

    try:
        #page_driver = webdriver.Firefox()

        time.sleep(8)

        pop_up_window = WebDriverWait(page_driver, 2).until(EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'SPERR._R.z')))

        stop = 50
        current = 0

        img_base_urls_list = []
        start = time.time()

        while current-start<stop:
            current = time.time()
            time.sleep(10)
            img_divs = page_driver.find_elements(By.CLASS_NAME,'cfCAA.w._Z.GA')
            for i in set(img_divs):
                img_base_urls_list.append(i.get_attribute('style').split('"')[1])
            page_driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',pop_up_window)

        img_base_urls = set(img_base_urls_list)

        base_url = 'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/'
        hrefs = []

        for raw_img_url in img_base_urls:
            img_url_words = raw_img_url.split('/')[-5:]
            img_url = '/'.join(img_url_words)
            
            hrefs.append(base_url+img_url + f'?w={image_width}&h=-1&s=1"')

        #print('hrefs', len(hrefs))

        
        #time.sleep(10)
        page_driver.close()
        page_driver.quit()
        
        return hrefs
    except Exception as e:
        print('img_base_urls', img_base_urls)
        print("exception occured", e)
        print("url", hotel_page_url)

        #time.sleep(10)
        page_driver.close()
        page_driver.quit()


def downloader(url, download_path, COUNTER, worker_no):
    

    failures = 0

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
    if worker_no == 2:
        print("Total Number of images in folder ", len(os.listdir(download_path)))
    try:
        if worker_no == 2:
            print("!!!!!!!!!!!!!!")
            print("stuck at image_content")
        image_content = requests.get(url[0], headers=headers).content
        if worker_no == 2:
            print("!!!!!!!!!!!!!!")
            print("stuck at image_file")
        image_file = io.BytesIO(image_content)
        if worker_no == 2:
            print("!!!!!!!!!!!!!!")
            print("stuck at image")
        image = Image.open(image_file)
        file_path = download_path + str(COUNTER)+'_'+str(worker_no) +'.jpg'
        with open(file_path, "wb") as f:
            print(f"{str(COUNTER)+'_'+str(worker_no) +'.jpg'} saved" )
            image.save(f, "JPEG")
    except:
        failures+=1
        print('failures: ', failures)
        print(url)




    

