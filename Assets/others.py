from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import *
import zipfile
import time
import json
import os

def acp_api_send_request(driver, message_type, data={}):
    message = {
        # всегда указывается именно этот получатель API сообщения
        'receiver': 'antiCaptchaPlugin',
        # тип запроса, например setOptions
        'type': message_type,
        # мерджим с дополнительными данными
        **data
    }
    # выполняем JS код на странице
    # а именно отправляем сообщение стандартным методом window.postMessage
    return driver.execute_script("""
    return window.postMessage({});
    """.format(json.dumps(message)))

def get_chromedriver(manifest_json=None, background_js=None, host=None, use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension(os.path.abspath('anticaptcha-plugin_v0.52.zip'))
    if use_proxy:
        pluginfile = f'proxy_auth_plugin_{host.replace(".","_").replace(":", "_")}.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(
        executable_path=os.path.abspath('chromedriver.exe'),
        chrome_options=chrome_options)
    return driver

def start_vk(proxy=None):
    if proxy:
        PROXY_HOST = proxy[0][:proxy[0].find(':')]  # rotating proxy or host
        PROXY_PORT = proxy[0][proxy[0].find(':') + 1:]  # port
        PROXY_USER = proxy[1] # username
        PROXY_PASS = proxy[2]  # password
        print(PROXY_HOST)
        print(PROXY_PORT)
        print(PROXY_USER)
        print(PROXY_PASS)
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
    
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
    
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
        # driver = get_chromedriver(manifest_json,background_js, use_proxy=True)
        # options = webdriver.ChromeOptions()
        # if proxy is not None:
        #     options.add_argument(f"--proxy-server={proxy}")
        # options.add_extension(os.path.abspath('anticaptcha-plugin_v0.52.zip'))
        browser = get_chromedriver(manifest_json=manifest_json, background_js=background_js, host=proxy[0], use_proxy=True)
    else:
        browser = get_chromedriver()
    browser.get('https://antcpt.com/blank.html')
    acp_api_send_request(
        browser,
        'setOptions',
        {'options': {'antiCaptchaApiKey': 'e92ddf1810917805c087ebc0079fc751'}}
    )
    time.sleep(3)
    browser.get("https://yandex.ru/internet")
    time.sleep(2)
    browser.get("https://vk.com/")
    return browser

def check_field(field):
    if field == '' or field is None:
        raise TypeError