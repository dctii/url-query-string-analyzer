import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.opera.options import Options as OperaOptions
# from msedge.selenium_tools import EdgeOptions

# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

load_dotenv()
SCHEME = os.getenv('SCHEME')
PROXY_HOST = os.getenv('MITMPROXY_HOST')
PROXY_PORT = os.getenv('MITMPROXY_PORT')
MITMPROXY_CER = os.getenv('MITMPROXY_CER')
MITMPROXY_PEM = os.getenv('MITMPROXY_PEM')
# BROWSER_ABS_PATH = os.getenv('BROWSER_PATH')

def chrome_opts(proxy, headless):
    chrome_options = ChromeOptions()

    if headless == 'headless-on':
        chrome_options.add_argument('--headless')
    elif headless == 'headless-off':
        pass

    if proxy == 'proxy-off':
        chrome_options.add_argument('--no-proxy-server')
    elif proxy == 'proxy-on':
        chrome_options.add_argument(f'--proxy-server={SCHEME}://{PROXY_HOST}:{PROXY_PORT}')
    elif proxy == 'proxy-auto':
        chrome_options.add_argument('--proxy-auto-detect')
    else:
        pass

    chrome_options.add_argument(f'--cert-server-certificate={MITMPROXY_CER}')
    chrome_options.add_argument(f'--cert-client-key={MITMPROXY_PEM}')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--enable-automation')
    chrome_options.add_argument('--test-type=webdriver')
    chrome_options.add_argument('--disable-sync')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-background-networking')
    chrome_options.add_argument('--disable-client-side-phishing-detection')
    # More options can be added if needed

    return chrome_options


def firefox_opts(proxy, headless):
    firefox_options = FirefoxOptions()

    if headless == 'headless-on':
        firefox_options.add_argument('-headless')
    elif headless == 'headless-off':
        pass
    if proxy == 'proxy-off':
        firefox_options.set_preference('network.proxy.type', 0)
    elif proxy == 'proxy-on':
        firefox_options.set_preference('network.proxy.type', 1)
        firefox_options.set_preference('network.proxy.http', PROXY_HOST)
        firefox_options.set_preference('network.proxy.http_port', PROXY_PORT)
        firefox_options.set_preference('network.proxy.ssl', PROXY_HOST)
        firefox_options.set_preference('network.proxy.ssl_port', PROXY_PORT)
    else:
        pass
    
    # More options can be added if needed

    return firefox_options

# TODO: Fix issues with options on other browsers. Prioritize Safari
"""
# DEBUG: Need to find out why options aren't working for Opera
def opera_opts(proxy, headless):
    opera_options = OperaOptions()

    if headless == 'headless-on':
        opera_options.add_argument('--headless')
    elif headless == 'headless-off':
        pass

    if proxy == 'proxy-off':
        opera_options.add_argument('--no-proxy-server')
    elif proxy == 'proxy-on':
        opera_options.add_argument(f'--proxy-server={SCHEME}://{PROXY_HOST}:{PROXY_PORT}')
    else:
        pass

    opera_options.add_argument(f'--cert-server-certificate={MITMPROXY_CER}')
    opera_options.add_argument(f'--cert-client-key={MITMPROXY_PEM}')
    opera_options.add_argument('--disable-popup-blocking')
    opera_options.add_argument('--disable-web-security')
    opera_options.add_argument('--enable-automation')
    opera_options.add_argument('--test-type=webdriver')
    opera_options.add_argument('--disable-sync')
    opera_options.add_argument('--disable-gpu')
    opera_options.add_argument('--disable-background-networking')
    opera_options.add_argument('--disable-client-side-phishing-detection')

    return opera_options


# DEBUG: Find out why Edge browser isn't working first; look at msedge-selenium-tools package docs
# DEBUG: Find out what options are available for Edge;
def edge_opts(proxy, headless):
    edge_options = EdgeOptions()

    if headless == 'headless-on':
        edge_options.use_chromium = True
        edge_options.add_argument('--headless')
    elif headless == 'headless-off':
        pass

    if proxy == 'proxy-off':
        pass
    elif proxy == 'proxy-on':
        edge_options.use_chromium = True
        edge_options.add_argument(f'--proxy-server={SCHEME}://{PROXY_HOST}:{PROXY_PORT}')
    else:
        pass

    return edge_options




# DEBUG: selenium.webdriver.safari has no "Options"
# def safari_opts(proxy, headless):
#     safari_options = webdriver.SafariOptions()
    
#     safari_options.set_capability("safari:automaticInspection", True)
#     safari_options.set_capability("safari:automaticProfiling", True)
#     safari_options.set_capability("safari:useSimulatedTimers", True)
#     safari_options.set_capability("safari:cleanSession", True)

    # TODO: Not sure safari can be ran headlessly. So may need to just remove this or just set it to "pass"
#     if headless == 'headless-on':
#         safari_options.add_argument('--headless')
#     elif headless == 'headless-off':
#         pass

#     if proxy == 'proxy-off':
#         pass
#     elif proxy == 'proxy-on':
        # TODO: Sort out how to return the proxy as an option, may need to set another func for a desired capability, like def safari_dc(proxy)
#       PROXY = f"{PROXY_HOST}:{PROXY:PORT}"
#       webdriver.DesiredCapabilities.SAFARI['proxy'] = {
#         "httpProxy": PROXY,
#         "ftpProxy": PROXY,
#         "sslProxy": PROXY,
#         "proxyType": "MANUAL",
#         }
#     else:
#         pass

#     return safari_options
"""