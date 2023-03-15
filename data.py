from tools.functions import parse_ga_key

# Hostname
hostname = 'https://www.opera.com'

# Paths List. Will be combined with hostname to build a URL list

# Test path for tools.parse_ga_key
test_ga_path = "/j/collect?v=1&_v=j99&a=337605362&t=pageview&_s=1&dl=https%3A%2F%2Fwww.opera.com%2F&ul=en-us&de=UTF-8&dt=Opera%20Web%20Browser%20%7C%20Faster%2C%20Safer%2C%20Smarter%20%7C%20Opera&sd=24-bit&sr=1920x1080&vp=1905x391&je=0&_u=YEBAAEABAAAAACAAI~&jid=1207822036&gjid=1657180002&cid=1523548997.1678848216&tid=UA-4118503-39&_gid=931287793.1678848216&_r=1&_slc=1&gtm=45He33d0n81PRBZ42F&z=1016514567"

# Test URL for tools.go_to_url
test_url = 'https://www.opera.com'


# Smaller RL Test Lists for debugging
# parse_ga_key() is used here to test if it can parse and decode the URL from the query string parameter of the GA URL. 'dl' is the key for the URL the GA Tag is for.
url_test_list1 = [
  'https://www.opera.com/',
  'https://www.cpanel.net/'
]

url_test_list2 = [
  parse_ga_key(test_ga_path, 'dl'), # should parse https://www.opera.com/
  'https://www.google.com',
]
