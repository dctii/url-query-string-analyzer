import subprocess
import time
import os
import re
import csv
import shutil
import textwrap
import urllib.parse
from types import SimpleNamespace

import pandas as pd

from dotenv import load_dotenv

from mitmproxy import ctx

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchWindowException
from selenium.webdriver.common.by import By

from browser_options import (
  chrome_opts,
  firefox_opts,
  # TODO: Fixing these/seeing what's possible
  # safari_opts,
  # opera_opts,
  # edge_opts
  )

# ANSI Escape Codes for colored terminal formatting
ansi = SimpleNamespace(
    # Text colors
    BL="\033[30m", # BLACK
    R="\033[31m", # RED
    GR="\033[32m", # GREEN
    Y="\033[33m", # YELLOW
    B="\033[34m", # BLUE
    M="\033[35m", # MAGENTA
    C="\033[36m", # CYAN
    W="\033[37m", # WHITE
    RST="\033[39m", # RESET
    
    # Text colors (high intensity)
    HIR="\033[91m",
    HIG="\033[92m",
    HIY="\033[93m",
    HIB="\033[94m",
    HIM="\033[95m",
    HIC="\033[96m",
    HIW="\033[97m",
    
    # Background colors
    BGBL="\033[40m",
    BGR="\033[41m",
    BGGR="\033[42m",
    BGY="\033[43m",
    BGB="\033[44m",
    BGM="\033[45m",
    BGC="\033[46m",
    BGW="\033[47m",
    BGRST="\033[49m",
    
    # Background colors (high intensity)
    BGHIBL="\033[100m",
    BGHIR="\033[101m",
    BGHIGR="\033[102m",
    BGHIY="\033[103m",
    BGHIB="\033[104m",
    BGHIM="\033[105m",
    BGHIC="\033[106m",
    BGHIWH="\033[107m",
    
    # Text styles
    BD="\033[1m", # BOLD
    IT="\033[3m", # ITALIC
    ST="\033[9m", # STRIKETHROUGH
    D="\033[2m", # DIM
    U="\033[4m", # UNDERLINE
    BK="\x1b[5m", # BLINK
    RV="\033[7m", #REVERSE
    HDN="\033[8m", # HIDDEN
    RST_BK="\x1b[25m", # RESET BLINK
    RST_ALL="\033[0m", # RESET ALL
    
    # Cursor movements
    CURSOR_UP="\033[{n}A",
    CURSOR_DOWN="\033[{n}B",
    CURSOR_FORWARD="\033[{n}C",
    CURSOR_BACKWARD="\033[{n}D",
    CURSOR_POSITION="\033[{row};{column}H",
    SAVE_CURSOR_POSITION="\033[s",
    RESTORE_CURSOR_POSITION="\033[u",
    
    # Screen operations
    CLEAR_SCREEN="\033[2J",
    CLEAR_SCREEN_UP="\033[1J",
    CLEAR_SCREEN_DOWN="\033[J",
    CLEAR_LINE="\033[2K",
    CLEAR_LINE_START="\033[1K",
    CLEAR_LINE_END="\033[K",
    
    # Other
    SCROLL_UP="\033[{n}S",
    SCROLL_DOWN="\033[{n}T",
)

load_dotenv()
psw = os.getenv('password')
BROWSER = os.getenv('BROWSER')
SCHEME = os.getenv('SCHEME')
MITMPROXY_HOST = os.getenv('MITMPROXY_HOST')
MITMPROXY_PORT = os.getenv('MITMPROXY_PORT')
MITMPROXY_CER = os.getenv('MITMPROXY_CER')
MITMPROXY_PEM = os.getenv('MITMPROXY_PEM')
BROWSER_ABS_PATH = os.getenv('BROWSER_ABS_PATH')

def sleep_sandwich(seconds):
  def decorator(func):
    def wrapper(*args, **kwargs):
      time.sleep(seconds)
      result = func(*args, **kwargs)
      time.sleep(seconds)
      return result
    return wrapper
  return decorator

def check_proxy_states(psw):
    # Build the command as a single string
    cmd = f"echo {psw} | sudo -S scutil --proxy | awk '/HTTPEnable :/{{print $3}}; /HTTPSEnable :/{{print $3}}'"

    # Run the command using subprocess
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = p.communicate()[0].decode().strip().split("\n")

    # Check if HTTP Proxy is enabled or disabled
    if int(output[0]) == 0:
        print(f"⨯ {ansi.R}HTTP Proxy is disabled.{ansi.RST}")
    else:
        print(f"✓ {ansi.GR}HTTP Proxy enabled.{ansi.RST}")

    # Check if HTTPS Proxy is enabled or disabled
    if int(output[1]) == 0:
        print(f"⨯ {ansi.R}HTTPS Proxy is disabled.{ansi.RST}")
    else:
        print(f"✓ {ansi.GR}HTTPS Proxy enabled.{ansi.RST}")

def enable_proxies(password, quiet=False):
    cmd = f"echo {password} | sudo -S networksetup -setwebproxy Wi-Fi {MITMPROXY_HOST} {MITMPROXY_PORT} && " \
          f"echo {password} | sudo -S networksetup -setsecurewebproxy Wi-Fi {MITMPROXY_HOST} {MITMPROXY_PORT}"
    
    if not quiet:
        print(f"{ansi.Y}Enabling web proxies...{ansi.RST}")
        
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
    
    if not quiet:
        print(f"{ansi.Y}\nChecking web proxies...{ansi.RST}\n")
        check_proxy_states(password)
        print(f"\n{ansi.GR}Web proxies enabled...{ansi.RST}\n")

@sleep_sandwich(1)
def disable_proxies(password, quiet=False):
    cmd = f"echo {password} | sudo -S networksetup -setwebproxystate Wi-Fi off && " \
          f"echo {password} | sudo -S networksetup -setsecurewebproxystate Wi-Fi off"

    # Run the command using subprocess
    subprocess.check_output(cmd, shell=True)

    if not quiet:
        print(f"{ansi.Y}\nDisabling web proxies...{ansi.RST}")
        print(f"{ansi.Y}\nChecking web proxies...{ansi.RST}\n")
        check_proxy_states(password)
        print(f"\n{ansi.GR}Web proxies disabled.{ansi.RST}\n")
      
    del password

# Generate URLs array
def url_set_builder(host, path_source, sheet_name=None):
    if isinstance(path_source, list): # if it's an array
      path_list = path_source
    elif path_source.endswith('.csv'): # csv
        path_list = pd.read_csv(path_source).iloc[:, 0].tolist() # iloc locates the 0th col; after converts to Py list
    elif path_source.endswith('.xlsx') or path_source.endswith('.xls'): # excel file
        if sheet_name:
            path_list = pd.read_excel(path_source, sheet_name=sheet_name).iloc[:, 0].tolist()
        else:
            path_list = pd.read_excel(path_source).iloc[:, 0].tolist()
    else:
        raise ValueError("Invalid file or data type. Only CSV, Excel files, or Python Lists are supported.")
    
    # path_list = data_frame.iloc[:, 0].tolist()
    url_list = [f"{host}{path}" for path in path_list]
    return set(url_list)

# Go to a single URL
def go_to_url(url, ga_script_pattern, quiet=False, proxy='proxy-off', headless='headless-off', browser="Chrome"):
  try:
    # ua_str = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'

    # DEBUG -- not working
    if browser == "Firefox":
      opts = firefox_opts(proxy, headless)
      driver = webdriver.Firefox(options=opts)
    elif browser == "Safari":
      #TODO: Need to find out how to get it to stop asking "Continue Session" prompt on each browser opening
      #TODO: add options functionality for Safari
      
      # Shell execution to enable remote automation
      subprocess.run(['safaridriver', '--enable'])
      driver = webdriver.Safari()
    elif browser == "Chrome":
      print(browser)
      opts = chrome_opts(proxy, headless)
      driver = webdriver.Chrome(options=opts)

    # go to the URL
    driver.get(url)

    # wait for 10 seconds for the google-analytics element to be present
    wait = WebDriverWait(driver, 6)

    # Start a timer timer
    start_time = time.time()
    
    pattern = re.compile(fr'{ga_script_pattern}')

    try:
      wait.until(EC.presence_of_element_located((By.XPATH, f"//script[contains(text(),'{ga_script_pattern}')]")))
      element = wait.until(EC.presence_of_element_located((By.XPATH, f"//script[contains(text(),'{ga_script_pattern}')]")))

      if quiet == True:
        pass
      elif quiet == False:
        print(f"{ansi.GR}{ansi.BD}✓ '{ga_script_pattern}'{ansi.RST} detected in <script> tag:")
        print(f"Tag name: {element.tag_name}")
        print(f"Script content:")
        print("-"*50)
        print(f'<script type="text/javascript" id>')
        inner_html = element.get_attribute('innerHTML')
        highlighted_html = pattern.sub(f"{ansi.GR}{ansi.BD}{ga_script_pattern}{ansi.RST}", inner_html)
        print(f"{highlighted_html}")
        print(f'</script>')
        print("-"*50)
        print("\n")

    except TimeoutException:
        print(f"{ansi.R}{ansi.BD}⨯ Timed out waiting for google-analytics element{ansi.RST}\n")
    except WebDriverException as e:
          if isinstance(e, NoSuchWindowException):
              print(f"{ansi.R}{ansi.BD}⨯ Browser window was closed prematurely{ansi.RST}\n")
              print(f"{ansi.Y}Exiting the script.")
              exit(1)
          else:
              raise e
    finally:
        # Stop the timer and print the execution time
        end_time = time.time()
        if quiet == True:
          pass
        elif quiet == False:
          print(f"Script execution time: {end_time - start_time:.2f} seconds")

        # close the browser window
        time.sleep(2)
        # driver.quit()
  except KeyboardInterrupt:
    print(f"\n{ansi.R}{ansi.BD}⨯ Terminated with a KeyboardInterrupt.{ansi.RST}\n")
    exit(1)

def visit_all_urls(urls_array, ga_script_pattern, quiet=False, proxy='proxy-off', headless='headless-off', browser="Chrome"):
    for i, url in enumerate(urls_array):
      if quiet == True:
        pass
      elif quiet == False:
        iteration_num = f'#{i+1:03d}'
        wrapped_url = (f'\n {" "*4}').join(textwrap.wrap(url, width=31))
        print(f'{ansi.Y}{ansi.BD}\n ✦✦✦ {ansi.BK}⎨Running Iteration {iteration_num}{ansi.RST_BK}⎬ ✦✦✦{ansi.RST}\n')
        print(f'{" "*2}{ansi.B}{ansi.BD}{wrapped_url}{ansi.RST_ALL}\n')
      
      go_to_url(url, ga_script_pattern, quiet, proxy, headless, browser)
      
      if quiet == True:
        pass
      elif quiet == False:
        print(f'{ansi.GR}{ansi.BD} Script finished for:{ansi.RST}\n{ansi.B}{url}{ansi.RST}\n\n')

def parse_ga_key(path, key):
    decoded_path = urllib.parse.unquote_plus(path)
    decoded_path = decoded_path.replace("%2F", "/").replace('%3A', ':').replace('%25', '%').replace('%3B', ';').replace('%7C', '|').replace('%20', ' ')
    match = re.search(f"{key}=([^&]*)", decoded_path)
    if match:
        return match.group(1)
    else:
        return None
      
def parse_all_ga_keys(path):
    qsp = urllib.parse.urlparse(path).querys
    return dict(urllib.parse.parse_qsl(qsp))

def print_all_qsp_keys(path):
  ga_keys = parse_all_ga_keys(path)
  for key, value in ga_keys.items():
      print(f"{ansi.B}{key}{ansi.RST}: {ansi.Y}{value}{ansi.RST}")

def write_url_list(url_list, filename='output'):
  print(f'{ansi.Y}Writing to 01-{filename}.csv{ansi.RST}.')
  with open(f'01-{filename}.csv', 'w') as csvfile:
      csvwriter = csv.writer(csvfile)
      for url in url_list:
          csvwriter.writerow([url])
  print(f'{ansi.GR}Finished writing to 01-{filename}.csv{ansi.RST_ALL}.')  
  
def compare_url_lists(url_list_comparand, filename='output'):
    shutil.copyfile(f'01-{filename}.csv', f'02-{filename}_compared.csv')
    copied_file = f'{filename}_compared'
    
    print(f'{ansi.Y}Reading 02-{copied_file}.csv{ansi.RST_ALL}. Finding rows.')
    with open(f'02-{copied_file}.csv', 'r') as csvfile:
      rows = list(csv.reader(csvfile))
      non_list = []
      for i in range(0, len(rows)):
        if rows[i][0] in url_list_comparand:
          rows[i][0] = f'🟢 {rows[i][0]}'
        else:
          non_list.append(rows[i][0])
          rows[i][0] = f'🟠 {rows[i][0]}'
    
    print(f'{ansi.Y} Prepending "🟢" to matching URLs in {ansi.IT}"02-{copied_file}.csv"{ansi.RST_ALL}')
    with open(f'02-{copied_file}.csv', 'w', newline='') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerows(rows)
      
    print(f'{ansi.Y} Writing URLs not present in both lists to {ansi.IT}"03-{filename}_non_list.csv"{ansi.RST_ALL}')
    with open(f'03-{filename}_non_list.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for url in non_list:
            csvwriter.writerow([url]) 

def countdown(duration, type=None):
  if type == 'mitm':
    for i in range(duration, 0, -1):
      ctx.log.warn(f"\n\nTime left: {i} seconds\n\n")
      time.sleep(1)
      ctx.log.alert(f"\n\nTime's up!\n\n")
  elif type==None:
    for i in range(duration, 0, -1):
      print(f"{ansi.Y}Time left: {i} seconds{ansi.RST}")
      time.sleep(1)
    print(f"{ansi.GR}{ansi.BK}Time's up!{ansi.RST_ALL}")

