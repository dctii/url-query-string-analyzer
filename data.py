from tools.functions import parse_ga_key

# Hostname
hostname = 'https://www.opera.com'

# Paths List. Will be combined with hostname to build a URL list
path_list = [
  '',
  '/products',
  '/gaming',
  'browsers/opera',
  '/crypto/next',
  '/download',
  '/about',
  '/help'
]


# Test path for tools.parse_ga_key
test_ga_path = "/j/collect?v=1&_v=j99&a=337605362&t=pageview&_s=1&dl=https%3A%2F%2Fwww.opera.com%2F&ul=en-us&de=UTF-8&dt=Opera%20Web%20Browser%20%7C%20Faster%2C%20Safer%2C%20Smarter%20%7C%20Opera&sd=24-bit&sr=1920x1080&vp=1905x391&je=0&_u=YEBAAEABAAAAACAAI~&jid=1207822036&gjid=1657180002&cid=1523548997.1678848216&tid=UA-4118503-39&_gid=931287793.1678848216&_r=1&_slc=1&gtm=45He33d0n81PRBZ42F&z=1016514567"

test_ga_path2 = '/g/collect?v=2&tid=G-T18E1GTPQG&gtm=45je33d0&_p=376870707&cid=1523548997.1678848216&ul=en-us&sr=2560x1440&uaa=arm&uab=64&uafvl=Google%2520Chrome%3B111.0.5563.64%7CNot(A%253ABrand%3B8.0.0.0%7CChromium%3B111.0.5563.64&uamb=0&uam=&uap=macOS&uapv=13.2.1&uaw=0&_s=1&sid=1678896887&sct=3&seg=1&dl=https%3A%2F%2Fwww.opera.com%2F&dt=Opera%20Web%20Browser%20%7C%20Faster%2C%20Safer%2C%20Smarter%20%7C%20Opera&en=page_view'

test_ga_path3 = '/j/collect?v=1&_v=j99&a=500362506&t=pageview&_s=1&dl=https%3A%2F%2Fwww.opera.com%2Fhelp&ul=en-us&de=UTF-8&dt=Browser%20Problems%3F%20We%20can%20help%20you!%20%7C%20Help%20%26%20FAQ%20%7C%20Opera&sd=24-bit&sr=2560x1440&vp=1398x354&je=0&_u=QACAAEABAAAAACAAI~&jid=2136327141&gjid=1745991188&cid=1523548997.1678848216&tid=UA-4118503-39&_gid=931287793.1678848216&_r=1&_slc=1&gtm=45He33d0n81PRBZ42F&cd3=1523548997.1678848216&z=1695587135'

test_ga_path4 = '/j/collect?t=dc&aip=1&_r=3&v=1&_v=j99&tid=UA-4118503-39&cid=1523548997.1678848216&jid=2136327141&gjid=1745991188&_gid=931287793.1678848216&_u=QACAAEAAAAAAACAAI~&z=896496708'

test_ga_path5 = 'g/collect?v=2&tid=G-T18E1GTPQG&gtm=45je33d0&_p=500362506&cid=1523548997.1678848216&ul=en-us&sr=2560x1440&uaa=arm&uab=64&uafvl=Google%2520Chrome%3B111.0.5563.64%7CNot(A%253ABrand%3B8.0.0.0%7CChromium%3B111.0.5563.64&uamb=0&uam=&uap=macOS&uapv=13.2.1&uaw=0&_s=1&sid=1678896887&sct=3&seg=1&dl=https%3A%2F%2Fwww.opera.com%2Fhelp&dr=https%3A%2F%2Fwww.opera.com%2Fgaming&dt=Browser%20Problems%3F%20We%20can%20help%20you!%20%7C%20Help%20%26%20FAQ%20%7C%20Opera&en=page_view'

# Test URL for tools.go_to_url
test_url = 'https://www.opera.com'


# Smaller RL Test Lists for debugging
# parse_ga_key() is used here to test if it can parse and decode the URL from the query string parameter of the GA URL. 'dl' is the key for the URL the GA Tag is for.
url_test_list1 = [
  'https://www.opera.com/',
  'https://www.cpanel.net/'
  'https://www.opera.com/products',
]

url_test_list2 = [
  parse_ga_key(test_ga_path, 'dl'), # should parse https://www.opera.com/
  'https://www.google.com',
  'https://www.opera.com/products'
]
