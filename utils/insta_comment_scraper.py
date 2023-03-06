from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait      
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from dateutil.parser import parse
from time import sleep
from selenium.common.exceptions import WebDriverException
from dotenv import load_dotenv
import os
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()
load_dotenv()
username = os.getenv('username')
password = os.getenv('password')
print('username:',username)

def comment_scraper(url: str, user_name = username, pass_word = password):
    print('user_name:', user_name)
    try:
        print('start')
        print('url:', url)
        comment_list = []
        last_list = []

        #Instance of Chrome driver and connection to url
        options = webdriver.ChromeOptions() 
        options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")
        options.add_experimental_option('detach', True) #Path to your chrome profile
        options.add_argument("user-data-dir=/tmp/.com.google.Chrome.ig41PN/Default")
        options.add_argument('--no-sandbox')
        options.add_argument ('--headless=new')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        #Wait for page loading
        driver.implicitly_wait(5)

        print('clicking on cookies...')
        content1 = driver.page_source.encode("utf-8")
                # with open ('page.txt', 'w') as file:
                #     file.write(content.decode('utf-8'))
        print('page content1:', content1.decode('utf-8'))

        if len(driver.find_elements(By.XPATH, "//div[text()='HTTP ERROR 429']"))>0:
            print('Sleeping... It will start again in 15 minutes.')
            driver.close()
            sleep(900)
            return comment_scraper(url)
        else:
            # Click on cookies window to access the page if exists
            if len(driver.find_elements(By.XPATH,"//button[contains(@class,'_a9-- _a9_1')]")) > 0:
                driver.find_element(By.XPATH,"//button[contains(@class,'_a9-- _a9_1')]").click()
                driver.implicitly_wait(5)
                print('cookies clicked')
                # 
            else:
                pass
                       
            #Click on login button if appears
            if len(driver.find_elements(By.XPATH,"//a[text()='Log in']")) > 0:
                button = driver.find_element(By.XPATH,"//a[text()='Log in']")
                #Use this way to fix ElementClickInterceptedException error
                driver.execute_script("arguments[0].click();", button)
                #Place where you put your credentials 
                username = driver.find_element(By.NAME, 'username')
                password = driver.find_element(By.NAME, 'password')
                username.send_keys(user_name)
                password.send_keys(pass_word)
                login_button = driver.find_element(By.XPATH,"//div[text()='Log in']")
                #Use this way to fix ElementClickInterceptedException error
                driver.execute_script("arguments[0].click();", login_button)
                print('logged in')
                content = driver.page_source.encode("utf-8")
                # with open ('page.txt', 'w') as file:
                #     file.write(content.decode('utf-8'))
                print('page content:', content.decode('utf-8'))
            else:
                pass

            # Check if "Load more comments" exists, if so click
            while len(driver.find_elements(By.XPATH,"//*[name()='svg' and @aria-label='Load more comments']")) > 0:
                more_comments_button = driver.find_element(By.XPATH,"//*[name()='svg' and @aria-label='Load more comments']")
                #Use this way to fix ElementClickInterceptedException error
                more_comments_button.click()
            else:
                # Get comments and dates of the post
                print('end of comments')
                comments = driver.find_elements(By.XPATH,"//span[contains(@class, '_aacl _aaco')]")
                date_time = driver.find_elements(By.XPATH,"//time[contains(@class, '_a9ze _a9zf')]")
                for com in comments:
                    comment_list.append(com.get_attribute("innerText"))
                for i in range(1,len(date_time)):
                    datetime = parse(date_time[i].get_attribute("datetime"))
                    date = datetime.strftime('%m-%d-%Y')
                    time = datetime.strftime('%H:%M:%S')
                    comment_details= {'url': url, 'comment':comment_list[i-1], 'date':date, 'time': time}
                    print('details:',comment_details)
                    last_list.append(comment_details)
            driver.close()
            return last_list
    except WebDriverException:
        return 'Please try again'

if __name__ == '__main__':
    urls = ['https://www.instagram.com/p/Ca2IjSygvyC', 'https://www.instagram.com/p/CXjUkf6IXHc','https://www.instagram.com/p/CZM8JxdBj5e']
    for url in urls:
        comment_scraper(url)

  