# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest, time, re
from pyvirtualdisplay import Display
import csv
import logging
logger = logging.getLogger(__name__)

class Tutorindia(unittest.TestCase):

    def setUp(self):
        logger.debug("I'm init.")

        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(1)
        logger.debug("Init: good.")

    def how_much_pages(self):
        number_of_pages = None
        try:
            text_with_number = self.driver.find_element_by_xpath('//*[@id="outercontainer"]/div[1]/div/div[4]/p/b').text
            number_of_tutors = int(re.findall(r'of (.*?)\)', text_with_number, re.DOTALL)[0])
            number_of_pages = int(number_of_tutors / 25)
        except:
            pass
        return number_of_pages

    def get_info_from_25_prof(self, driver):
        profiles = []
        for i in range(6, 36):
            try:
                profiles.append(driver.find_element_by_xpath(
                    '//*[@id="outercontainer"]/div[1]/div/div[' + str(i) + ']/div[1]/div[1]/a').get_attribute("href"))
            except:
                pass
        for profile in profiles:
            driver.get(profile)
            try:
                with open('result_1.csv', 'a') as csvfile:
                    fieldnames = ('name', 'photo', 'Subject', 'specialization_description', 'additional_info', 'headline', 'education', 'feedback', 'city', 'url', 'gender', 'pin_code', 'phone')
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    try:
                        photo = driver.find_element_by_xpath('//*[@id="outermain"]/div[1]/div/div[8]/img').get_attribute("src")
                    except:
                        photo = ''
                    a = {'name': driver.find_element_by_xpath('//*[@id="outermain"]/div[1]/div/div[3]/div[1]/h2/span').text,
                         'photo': photo,
                         'Subject': driver.find_element_by_xpath('//*[@id="outermain"]/div[1]/div/div[6]').text,
                         'specialization_description': driver.find_element_by_xpath('//*[@id="outermain"]/div[1]/div/p[5]/span').text,
                         'additional_info': driver.find_element_by_xpath('//*[@id="outermain"]/div[1]/div/p[6]').text,
                         'headline': driver.find_element_by_xpath('//*[@id="outermain"]/div[1]/div/div[7]/h1/i/span').text,
                         'education': driver.find_element_by_xpath('//*[@id="outermain"]/div[1]/div/p[3]').text,
                         'feedback': '',
                         'city': driver.find_element_by_xpath('//*[@id="outermain"]/div[1]/div/div[16]/p[1]/span[1]').text,
                         'url': profile,
                         'gender': driver.find_element_by_xpath('//*[@id="outermain"]/div[1]/div/p[13]/span').text,
                         'pin_code': driver.find_element_by_xpath('//*[@id="outermain"]/div[1]/div/div[16]/p[2]').text,
                         'phone': driver.find_element_by_xpath('//*[@id="outermain"]/div[1]/div/div[16]/p[3]/span').text,
                         }
                    writer.writerow(a)
                    csvfile.close()
            except:
                pass

    def get_city_links(self, driver):
        city_links = []
        for m in range(1, 500):
            try:
                city_links.append(driver.find_element_by_xpath('//*[@id="outercontainer"]/div[1]/div/div[4]/ul/li/a[' + str(m) + ']').get_attribute("href"))
            except:
                return city_links


    def test_tutorindia(self):
        driver = self.driver
        num_lines = sum(1 for line in open('English.txt'))
        lines = 1
        need_close_popap = True
        while lines != num_lines:
            with open('English.txt', 'r') as fin:
                data = fin.read().splitlines(True)
            with open('English.txt', 'w') as fin:
                fin.writelines(data[1:])
            url = data[0]

            print '\x1b[6;30;42m' + 'city_url' + '\x1b[0m', url
            driver.get(url)
            if need_close_popap:
                time.sleep(5)
                driver.find_element_by_css_selector("a.boxclose").click()
                need_close_popap = False


            how_much_pages = self.how_much_pages()
            if how_much_pages != None:
                self.get_info_from_25_prof(driver)
                current_page = 2
                while current_page < how_much_pages:
                    print '\x1b[6;30;42m' + 'current_page: ' + '\x1b[0m', current_page
                    driver.get(url+'-p'+str(current_page))
                    self.get_info_from_25_prof(driver)
                    current_page += 1
            lines += 1

if __name__ == "__main__":
    unittest.main()
