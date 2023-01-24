import os
import sys
import json
from pathlib import Path

from breaker_core.common.tools_identity import ToolsIdentity
from breaker_core.datasource.bytessource_file import BytessourceFile
from breaker_selenium.common.system_webdriver import SystemWebdriver
from breaker_selenium.economist.tab_manager_economist import TabManagerEconomist

if __name__ == '__main__':
    path_file_config_breaker = Path(os.getenv('PATH_FILE_CONFIG_BREAKER', 'config.cfg'))
    path_dir_data = Path(os.getenv('PATH_DIR_DATA_BREAKER', '/data/data_breaker/' ))
    path_file_webdriver = Path(os.getenv('PATH_FILE_WEBDRIVER', '/data/data_breaker/' ))
    with open(path_file_config_breaker, 'r') as file:
        dict_config = json.load(file)

    id_identity = 'identity_jaap_oosterbroek'
    identity = ToolsIdentity.identity_load(path_dir_data, id_identity)
    webdriver = ToolsIdentity.webdriver_load(path_dir_data, path_file_webdriver, id_identity)


    email = identity['economist_username']
    password = identity['economist_password']

    handle_builtin = webdriver.window_handles[0]
    tab_manager = TabManagerEconomist(dict_config, webdriver, handle_builtin) 

    path_file_edition = Path('edition.json')
    if not path_file_edition.is_file():
        list_edition_reference = tab_manager.action_list_edition_reference(identity)
        with path_file_edition.open('w') as file:
            json.dump(list_edition_reference, file)
    with path_file_edition.open('r') as file:
        list_edition_reference = json.load(file)

    path_file_article = Path('article.json')
    if not path_file_article.is_file():
        list_article_reference = tab_manager.action_list_article_reference(identity, list_edition_reference[0])
        for article_reference in list_article_reference:
            print(article_reference['subheadline'] + ' : ' + article_reference['headline'])
        with path_file_article.open('w') as file:
            json.dump(list_article_reference, file)

    with path_file_article.open('r') as file:
        list_article_reference = json.load(file)

    print(list_edition_reference[0])    
    print(list_article_reference[10])
    exit()
    bytessource = BytessourceFile(Path('article.mp3'), [])
    tab_manager.action_scrape_article_audio(identity, article_reference, bytessource)