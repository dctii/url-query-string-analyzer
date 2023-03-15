from dotenv import load_dotenv
import os
import time
from mitmproxy import ctx, flow
from mitmproxy.http import HTTPFlow
from mitmproxy.script import concurrent

from data import (
    url_test_list1 as list1,
    hostname,
    path_list,
)
from tools.functions import (
    ansi,    
    enable_proxies,
    disable_proxies,
    url_set_builder,
    write_url_list,
    compare_url_lists
)

# Initialize .env
load_dotenv()
psw = os.getenv('password')

# Initialize empty set for URLs that are detected to have target query string parameters with 'google-analytics.com' as domain
satisfactory_urls = set()

"""
Type in the name of this script to run it with mitmproxy; command in the line below
    `mitmproxy -s script.py --listen-host $(ipconfig getifaddr en0) -p 8081 --anticache`
    
- Selenium script to automate URL visitation must be ran separately, after mitmproxy has been activated and is listening.
- Do not exit the script while mitmproxy is active or else it will disrupt the process and the compare_url_list function will export an inaccurate output.
"""

class HTTPInterceptor:
    def __init__(self):
        # Prompt messages and web proxy enabling
        print(f'{ansi.Y}{ansi.BD}Initializing mitmproxy...{ansi.RST_ALL}')
        enable_proxies(psw, False)
        time.sleep(1)
        print(f'\n{ansi.B}{ansi.BD}Opening mitmproxy...{ansi.RST_ALL}\n')
        time.sleep(1)
        
        # Build unique url set from host name and list of paths.
        url_set = url_set_builder(hostname, path_list) 
        
        # Write unique URL set to CSV file to be compared later.
        write_url_list(url_set)
    
    
    @concurrent
    def request(self, flow: HTTPFlow) -> None:
        # Set variables for different values contained in HTTP requests
        request, meth, url, host, path, q = (
            flow.request,
            flow.request.method,
            flow.request.pretty_url,
            flow.request.pretty_host,
            flow.request.path,
            dict(flow.request.query),
        )
        
        # Conditions to meet to add to Google Analytics URL, `ga_urls` list to be compared against entire `url_set`
        # !important -- change these to suit the interception parameters you want
        http_method = 'POST'
        target_domain1 = 'google-analytics.com'
        target_domain2 = 'analytics.google.com'
        target_path_lead = '/g/collect?v'
        url_key = 'dl'
        qsp_key = 'en' # qsp (query string parameter)
        value = 'page_view'
        
        if (meth == http_method and
            target_domain1 or target_domain2 in host and
            target_path_lead in path and
            q.get(qsp_key) == value):
            ctx.log.warn(f"Adding '{q.get(url_key)}' to 'ga_urls' set()")
            satisfactory_urls.add(q.get(url_key))

    @concurrent
    def response(self, flow: HTTPFlow) -> None:
        pass
    
    # General messages for error
    @concurrent
    def error(self, flow: HTTPFlow) -> None:
        ctx.log.error("An HTTP error has occured.")

    # When the exiting mitmproxy is finished, compare `url_set` against `ga_urls`, outputting differences into CSV files.
    # 02-...csv shows all URLs. Green met the condition. Orange did not and need to be looked at.
    # 03-...csv shows all that were orange in 02-...csv without the orange marker prepended.
    @concurrent
    def done(self):
        if not satisfactory_urls:
            print(f'{ansi.R}No satisfactory urls added to the list. Will not output any addtional CSVs.{ansi.RST}')
            pass
        else:
            compare_url_lists(satisfactory_urls)
        # Disable proxies
        disable_proxies(psw, False)


addons = [HTTPInterceptor()]
