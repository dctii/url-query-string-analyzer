# url-query-string-analyzer
 Built to analyze Google Analytics query string parameters.


### Brew packages to install:

- mitmproxy 9.0.1: `brew install mitmproxy`
- Python 3.11.x: `brew install python@3.11`
- google-chrome: `brew install --cask chromedriver`
- chromedriver: `brew install --cask chromedriver`
- firefox: `brew install --cask firefox`
- geckodriver: `brew install --cask geckodriver`


### Python3 Requirements

Major packages are `mitmproxy`, `selenium`, and `python-dotenv`. Others are needed, check the `requirements.txt` file. 

### Shell commands to run this application:

**If you do not already have a config.yaml, then run this command:**  

`mv config.yaml ~/.mitmproxy/config.yaml`

#### Running mitmproxy and loading it with a script


For the script name, do not add the extension. Just the name. So, don't put `script.py`, put `script` or whatever you may rename the file.

**Screen 1:**
```bash
source .venv/bin/activate
start-mitmproxy
	Would you like to add a script (y/n) y
	What is the name of the script? script
```

#### Running Selenium

**Screen 2:**
```bash
source .venv/bin/activate
python3 selen.py
```