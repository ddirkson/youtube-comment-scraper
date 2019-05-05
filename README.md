# youtube-comment-scraper
### A simple python script that uses selenium to scrape youtube comments

#### Selenium Installation:
```
pip install selenium
```
* Selenium Docs: https://selenium-python.readthedocs.io/installation.html#drivers
#### Installing A Webdriver:
* In order for the script to work, you'll also need to install a selenium-supported webdriver on your path
* For now, Google's chromedriver is the only webdriver used but support for others could be added in the future
* Chromedriver link: http://chromedriver.chromium.org/
* Currently, the script looks for the Google chrome binary (which you also need) at this location ```/usr/bin/google-chrome``` but that could also be configurable in the future

#### Current script workflow:
* Provide a youtube channel name
* The script creates a new directory with a name matching the channel name in the same directory that the script is in
* All of the channel's video urls are parsed and stored in a "channelname"_videos.txt file
* As the script processes videos, it adds processed urls to a "channelname"_videos_read.txt file
* Any comments that contain one of your specified keywords are written to a "channelname"_comments.txt file
* The comments file contains a header specifying the associated url for each set of keyword-matching comments

#### How to appropriately specify a channel to scrape:
* Youtube has dynamic channel ids for certain channels
* In the case of a dynamic channel id (can go to channel > videos and look at the value behind /channel/ in the url), the channel id will typically be a random string of characters e.g. UCptcwxWxukDu9hF313xfH0w
* The most accurate parsing results come from being able to specify a static channel id, but the script can handle dynamic ones as well
* Providing the dynamic flag "-d" will attempt to use youtube's search functionality and grab the first channel result that the search returns
* This is usually still accurate but once in awhile you'll have to double check that the urls being pulled in for a dynamic id channel actually correspond to the channel you were looking for
