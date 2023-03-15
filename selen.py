import os
from dotenv import load_dotenv

from data import (
  url_test_list1 as list1,
  url_test_list2 as list2,
  hostname,
  path_list,
)
from tools.functions import (
  url_set_builder,
  visit_all_urls
)

BROWSER = os.getenv('BROWSER')

# Build the URL list
list = url_set_builder(hostname, path_list)

# Visit all the URLs
visit_all_urls(list, 'sit-gaLoaded', False, 'proxy-on', 'headless-off', f"{BROWSER}")

# Test with a single URL instead
# go_to_url(test_url, False, 'proxy-on', 'headless-off')
