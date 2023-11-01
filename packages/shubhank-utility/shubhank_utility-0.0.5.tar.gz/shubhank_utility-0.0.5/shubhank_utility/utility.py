import re
import json
import base64
import requests
import pandas as pd
from tldextract import extract
from datetime import datetime

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import logging
logging.basicConfig(level=logging.ERROR)


def write_json(data, filename, mode="w"):
    """
    This function will create the json file.
    """
    try:
        with open(filename, mode, encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=True)
    
    except Exception as e:
        print(e)


def read_json(filename, mode="r"):
    """
    This function will read the json file.
    """
    data = None
    try:
        with open(filename, mode) as json_file:
            data = json.load(json_file)
    
    except Exception as e:
        print(e)

    finally:
        return data


def write_file(data, filename, mode="w"):
    """
    This function will create the file.
    """
    try:
        with open(filename, mode) as file:
            file.write(data)
    
    except Exception as e:
        print(e)


def read_file(filename, mode="r"):
    """
    This function will read the file.
    """
    data = None
    try:
        with open(filename, mode) as file:
            data = file.read()
    
    except Exception as e:
        print(e)

    finally:
        return data


def get_domain(data):
    """
    This function is to get domain from urls.
    Input can be a single string or a list of string.
    """

    if data:

        if isinstance(data, str):
            url = extract(data).registered_domain
            return url if url else data

        elif isinstance(data, list):

            domains = set()
            for item in data:

                try:
                    url = extract(data).registered_domain
                    out = url if url else item
                    domains.add(out)

                except Exception as e:
                    logging.error("error in parsing domain" + str(e))

            domains = list(domains)
            return domains[0] if len(domains) == 1 else domains

    return None


def get_website(data):
    """
    This function is to get standardized websites from urls.
    Input can be a single string or a list of string.
    """
    if data:

        if isinstance(data, str):
            # data = list(extract(data))
            # data[0] = "www" if data[0] == "" else data[0]
            # url = "https://" + ".".join(data)
            url = extract(data).fqdn
            return url if url else data

        elif isinstance(data, list):

            domains = set()
            for item in data:

                try:
                    # item_t = list(extract(item))
                    # item_t[0] = "www" if item_t[0] == "" else item_t[0]
                    # url = "https://" + ".".join(item_t)
                    url = extract(item).fqdn
                    out = url if url else item
                    domains.add(out)

                except Exception as e:
                    logging.error("error in parsing domain" + str(e))

            domains = list(domains)
            return domains[0] if len(domains) == 1 else domains

    return None


def try_encoding(data):
    """
    This function is to encode the data.
    """
    
    if not data:
        return data
    
    if not isinstance(data, str):
        return data
    
    try:
        try:
            try:
                tmp = data.encode().decode('utf-8').encode('cp1252').decode('utf-8').encode('cp1252').decode('utf-8')

            except Exception as e:
                tmp = data.encode().decode('utf-8').encode('cp1252').decode('utf-8')

        except Exception as e:
            tmp = data.encode().decode('utf-8')
            
    except Exception as e:
        tmp = data
    
    return tmp


def check(data, x):
    """
    This function is to check if key is present in dict and have a valid value or not.
    """
    if isinstance(data, dict) and data and x and x in data:
        if data[x] and str(data[x]) not in ["null", "None", "nan"]:
            return True
    return False


def check_dataframe(data):
    """
    This function is to check if data is a dataframe with atleast one element.
    """
    if isinstance(data, pd.core.frame.DataFrame) and any(data) and len(data) >= 1:
        return True
    return False


def check_list(data):
    """
    This function is to check if data is a list with atleast one element.
    """
    if data and isinstance(data, list) and len(data) >= 1:
        return True
    return False


def check_dict(data):
    """
    This function is to check if data is a dict with atleast one key value pair.
    """
    if data and isinstance(data, dict) and len(data) >= 1:
        return True
    return False


def sstrip(data):
    """
    This function strip the value if it is string.
    """
    if isinstance(data, str):
        data = data.strip()
    return data


def format_date(date, format="%y-%m-%d"):
    try:
        date = datetime.strptime(date, format)
    
    except Exception as e:
        print(e)
    
    finally:
        return date


def get_image(url):
    """
    This function will load the image from url and return base64 image.
    """
    return base64.b64encode(requests.get(url).content)


def camel_to_snake(string):
    """
    This function is to convert camelCase to snake_case.
    """
    try:
        if string and isinstance(string, str):
            string = "_".join(string.split())
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()
    
    except Exception as e:
        print(e)
    
    finally:
        return string


def record_error(error, filename="error.txt", mode="a"):
    """
    Function to record the error in a text file.
    """
    with open(filename, mode, encoding="utf-8") as file:
        file.write(str(error)+ "\n")


def get_browser(chrome_path="chromedriver.exe", headless=False):
    
    options = Options()
    if headless:
        options.add_argument("headless")

    browser = webdriver.Chrome(executable_path=chrome_path, chrome_options=options)
    browser.maximize_window()

    return browser