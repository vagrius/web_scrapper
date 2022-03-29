import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from post import auto_mailing


def site_scrapper():

    driver = webdriver.Chrome()
    driver.get('https://weather.com/')
    time.sleep(3)

    current_url = driver.current_url
    assert current_url.find('weather.com') != -1, 'Wrong URL'

    city_list = []
    output_general = []
    with open('input.csv') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                output_general.append(row)
            else:
                city_list.append(row[0])

    for city in city_list:
        input_field = driver.find_element(By.ID, 'LocationSearch_input')
        input_field.send_keys(city)
        time.sleep(3)

        search_result = driver.find_element(By.CSS_SELECTOR, '.SearchResults--SearchResults--LUsso').text

        if search_result.find('Результаты не найдены') != -1 or search_result.find('No results') != -1:
            output_general.append([
                city,
                '',
                '',
                '',
                '',
                '',
                '',
                '',
            ])
        else:
            first_element = driver.find_element(By.ID, 'LocationSearch_listbox-0')
            first_element.click()
            time.sleep(3)

            today_max_min = driver.find_element(By.CSS_SELECTOR, '.CurrentConditions--primary--2SVPh .CurrentConditions--tempHiLoValue--3SUHy').text.split()
            today_weather = driver.find_element(By.CSS_SELECTOR, '.CurrentConditions--primary--2SVPh .CurrentConditions--phraseValue--2Z18W').text

            driver.find_elements(By.CSS_SELECTOR, "#WxuLocalsuiteNav-header-71dadf79-621d-43ff-9a1a-d99a39f16abe .Button--default--3zkvy")[2].click()
            time.sleep(3)
            tomorrow_max_min = driver.find_element(By.CSS_SELECTOR, '#titleIndex1 .DetailsSummary--temperature--1Syw3').text.split('\n')

            output_general.append([
                city,
                today_max_min[1],
                today_max_min[4],
                today_weather,
                tomorrow_max_min[0],
                tomorrow_max_min[1].lstrip('/'),
                '?',
                '?',
            ])

        driver.find_elements(By.CSS_SELECTOR, "#WxuLocalsuiteNav-header-71dadf79-621d-43ff-9a1a-d99a39f16abe .Button--default--3zkvy")[0].click()
        time.sleep(3)

    print(*output_general, sep='\n')

    with open('output.csv', 'w', newline='') as out:
        writer = csv.writer(out)
        for row in output_general:
            writer.writerow(row)


if __name__ == "__main__":

    site_scrapper()
    auto_mailing()
