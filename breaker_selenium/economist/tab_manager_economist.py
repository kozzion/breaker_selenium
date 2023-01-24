
import os
import sys
import json
import time
import requests

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from breaker_core.datasource.bytessource import Bytessource

from breaker_selenium.common.system_webdriver import SystemWebdriver
from breaker_selenium.common.tab_manager_base import TabManagerBase

class TabManagerEconomist(TabManagerBase):

    def __init__(self, config:dict, webdriver: WebDriver, window_handle) -> 'None':
        super(TabManagerEconomist, self).__init__()
        self.config = config
        self.webdriver = webdriver
        self.window_handle = window_handle
 

    def action_list_edition_reference(self, identity):
        print('action_create_account')
        self.make_active()
        SystemWebdriver.open_url(self.webdriver, 'https://www.economist.com/weeklyedition/archive')
        SystemWebdriver.await_is_present(self.webdriver, 'edition-teaser')
        list_element_edition = self.webdriver.find_elements(By.CLASS_NAME, 'edition-teaser')
        print(len(list_element_edition))
        list_edition_reference = []
        for element_edition in list_element_edition:
            url_image = element_edition.find_element(By.TAG_NAME, 'img').get_attribute("src")
            url_edition = element_edition.find_element(By.CLASS_NAME, 'headline-link').get_attribute("href")
            id_edition = url_edition.split('/')[-1]

            edition_reference = {}
            edition_reference['id_edition'] = id_edition
            edition_reference['url_edition'] = url_edition
            edition_reference['url_image'] = url_image

            list_edition_reference.append(edition_reference)
        return list_edition_reference

    def action_list_article_reference(self, identity, edition_reference):
        print('action_create_account')
        self.make_active()
        SystemWebdriver.open_url(self.webdriver, edition_reference['url_edition'])
        SystemWebdriver.await_is_present(self.webdriver, 'weekly-edition-wtw__item')
        # list leaders section
        list_article_reference = []


        list_article_reference.extend(self.parse_section(self.webdriver, 'weekly-edition-wtw__item', 'world_this_week'))
        list_article_reference.extend(self.parse_section(self.webdriver, 'teaser-weekly-edition--leaders', 'leaders'))
        list_article_reference.extend(self.parse_section(self.webdriver, 'teaser-weekly-edition--briefing', 'briefing'))
        list_element_section = self.webdriver.find_elements(By.CLASS_NAME, 'layout-weekly-edition-section--cols')
        for element_section in list_element_section:
            name_section = element_section.find_element(By.CLASS_NAME, 'ds-section-headline').get_attribute("innerHTML")
            print(name_section)
            list_article_reference.extend(self.parse_section(element_section, 'teaser-weekly-edition--cols', name_section))
        return list_article_reference

    def get_attribute_default(self, source_element, by, by_argument, attribute, default=''):
        list_element = source_element.find_elements(by, by_argument)
        if len(list_element) != 1:
            return default
        try:
            return list_element[0].get_attribute(attribute)
        except Exception as e:
            return default


    def parse_section(self, source_element, name_class, name_section):
        list_element_article = source_element.find_elements(By.CLASS_NAME, name_class)
        list_article_reference = []
        for element_article in list_element_article:
            headline = self.get_attribute_default(element_article, By.CLASS_NAME, 'teaser__headline', "innerHTML")
            subheadline = self.get_attribute_default(element_article, By.CLASS_NAME, 'teaser__subheadline', "innerHTML")
            url_article = self.get_attribute_default(element_article, By.CLASS_NAME, 'headline-link', "href")
            article_reference = {}
            article_reference['name_section'] = name_section
            article_reference['name_section'] = name_section
            article_reference['url_article'] = url_article
            article_reference['headline'] = headline
            article_reference['subheadline'] = subheadline
            
            list_article_reference.append(article_reference)
        return list_article_reference

    def action_scrape_article_audio(self, identity:dict, article_reference:dict, bytessource_audio:Bytessource ):
        self.make_active()
        print(article_reference)
        print(article_reference['url_article'])
        SystemWebdriver.open_url(self.webdriver, article_reference['url_article'])
        SystemWebdriver.await_is_present(self.webdriver, 'weekly-edition-wtw__item')
        url_audio = self.webdriver.find_element(By.CLASS_NAME, 'react-audio-player').get_attribute("src")
        print(url_audio)

        response = requests.get(url_audio)
        if response.status_code == 200:
            bytessource_audio.write(response.content)
        else:
            print('fail')


