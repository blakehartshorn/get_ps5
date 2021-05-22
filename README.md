# get_ps5.py

### A nagios plugin to check for PS5 stock across major retailers

Requirements:
* Firefox
* [geckodriver](https://github.com/mozilla/geckodriver/releases)
* xvfb
* python3-selenium
* python3-requests
* pyvirtualdisplay

Or, just build the Docker container after copying the latest geckodriver into this folder.

`docker build -t get_ps5:latest .`

This plugin uses Firefox and Selenium to concurrently check Amazon, BestBuy, Gamestop, Target and Walmart. It uses requests to check Playstation Direct.

These checks all run concurrently, so allowing at least 4 cpu cores is preferred, although feel free to go higher.

I added the nagios user to the docker group and have Icinga running the command as follows:

`docker run --rm --cpus=8 --memory=8g get_ps5:latest`

Docker seemed to be the surefire way to make sure all Firefox sessions close, but running it directly on a host hasn't left any browser windows open for me so far. 
