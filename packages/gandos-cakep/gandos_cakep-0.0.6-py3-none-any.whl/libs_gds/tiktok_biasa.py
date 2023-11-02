from selenium import webdriver
import time
import requests
import json

## *********************************************************** SELENIUM
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
## *********************************************************** SELENIUM


class LibGds:

    def __init__(self, user, type_akun, dirImg):
        self.user=user
        self.type_akun=type_akun
        self.dirImg=dirImg

        options = webdriver.ChromeOptions()
        options.add_argument("--verbose")
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--window-size=1920, 1200")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)


    def set_cookies(self):
        self.driver.get("https://www.tiktok.com/")
        time.sleep(5)

        response_akun = requests.get("https://sistem.bebitesgroup.com/PROJECT/CPA/api_blast/?action=get_cookies_tiktok_update&user="+self.user+"&type_akun="+self.type_akun)
        json_akun   = response_akun.json()
        id_akun     = json_akun[0]["id_akun"]
        cookies     = json_akun[0]["cookies"]

        try:
            json_object = json.loads(cookies)
            for i in json_object:
                cookie_with_name_and_value = {
                    "name" : i["name"],
                    "value" : i["value"]
                }

                # print(cookie_with_name_and_value)
                self.driver.add_cookie(cookie_with_name_and_value)
        except:
            print("JSON BUSUK")

        self.driver.get("https://www.tiktok.com/creator-center/upload")
        time.sleep(3)

        url_bisnis_anyar = self.driver.current_url
        time.sleep(1)
        if(url_bisnis_anyar != "https://www.tiktok.com/creator-center/upload"):
            self.driver.get("https://www.tiktok.com/upload")
            print("URL UPLOAD LAWAS")
            time.sleep(2)

        x = 1
        try:
            frame = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='app']/div[3]/div/div/iframe"))
            )
            self.driver.switch_to.frame(frame)
            print("Frame APP 3")
            x = x-1
        except:
            print("Frame APP 3 KOSONG")

        try:
            frame = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='app']/div[2]/div/div/iframe"))
            )
            self.driver.switch_to.frame(frame)
            print("Frame APP 2")
            x = x-1
        except:
            print("Frame APP 2 KOSONG")

        try:
            frame = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div[2]/div[2]/div/div/iframe"))
            )
            self.driver.switch_to.frame(frame)
            print("Frame ROOT 2")
            x = x-1
        except:
            print("Frame ROOT 2 KOSONG")

        try:
            frame = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div[3]/div[2]/div/div/iframe"))
            )
            self.driver.switch_to.frame(frame)
            print("Frame ROOT 3")
            x = x-1
        except:
            print("Frame ROOT 3 KOSONG")


        if(x == 0):

            file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type=file]")
            all_path_images = r""+self.dirImg + "a (1).mp4"
            all_path_images = all_path_images.strip()
            file_input.send_keys(all_path_images)  

            time.sleep(5)

            el_edit_video = WebDriverWait(self.driver, 40).until(
                EC.visibility_of_element_located((By.XPATH, "//div[text()='Edit video']"))
            )
            el_edit_video.click()

            req_musik   = requests.get("https://sistem.bebitesgroup.com/PROJECT/CPA/api_blast/?action=get_mst_music")
            json_musik  = req_musik.json()
            judul_artis_01 = json_musik[0]["judul_artis"]
            judul_lagu  = json_musik[0]["judul_lagu"]
            judul_artis = judul_artis_01.strip()
            judul_lagu_01 = judul_lagu.strip()

            el_input_search = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='tux-portal-container']/div[2]/div/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[1]/div/div[2]/input"))
            )
            el_input_search.click()
            el_input_search.send_keys(judul_artis)
            
            el_btn_search = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[text()='Search']"))
            )
            el_btn_search.click()

            try:
                el_lagu = WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[text()='"+judul_lagu_01+"']"))
                )
                el_lagu.click()

                el_Use = WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[text()='Use']"))
                )
                el_Use.click()

                print("lagu nemu")
            except:
                print("lagu gak nemu")

            time.sleep(7)

            el_Save_Edit = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[text()='Save edit']"))
            )
            el_Save_Edit.click()

            # req_kata     = requests.get("http://localhost/GDS/kata.php")
            # json_kata    = req_kata.json()

            # req_hastag     = requests.get("http://localhost/GDS/hastag.php")
            # json_hastag    = req_hastag.json()

            # caption = json_kata + " " + json_hastag + "#programmerkuno"
            caption ="#programmerkuno"

            el_caption = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div[1]/div/div/div/div/div/div"))
            )
            el_caption.click()
            el_caption.send_keys(Keys.CONTROL + 'a' + Keys.NULL, caption)

            try:
                el_proggramerkuno = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//span[text()='programmerkuno']"))
                )
                el_proggramerkuno.click()
            except:
                print("hastag gak metu")

            el_submit_post = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[text()='Post']"))
            )
            el_submit_post.click()
            
            try:
                el_sukses = WebDriverWait(self.driver, 35).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[text()='Upload another video']"))
                )
                el_sukses.click()
                print("================+* SUKSES *+================")
            except:
                print("================+* GAGAL *+================")

            time.sleep(2)
            self.driver.quit()

        else:
            print("Frame Gak Onok")
            requests.get("https://sistem.bebitesgroup.com/PROJECT/CPA/api_blast/?action=update_akun_tiktok&id_akun="+id_akun)
            time.sleep(2)
            self.driver.quit()