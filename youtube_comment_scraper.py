#!/usr/bin/env python2

import os, time, argparse, socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def init_web_driver():
	chrome_options = Options()
	#  Optional argument to run the driver headlessly
	chrome_options.add_argument('--headless')
	chrome_options.binary_location = '/usr/bin/google-chrome'
	return webdriver.Chrome(chrome_options=chrome_options)

def scroll_to_bottom_of_page(web_driver):
	time.sleep(5)

	get_scroll_height_command = 'return (document.documentElement || document.body).scrollHeight;'
	scroll_to_command = 'scrollTo(0, {});'

	# Set y origin and grab the initial scroll height
	y_position = 0
	scroll_height = web_driver.execute_script(get_scroll_height_command)

	print 'Opened url, scrolling to bottom of page...'
	# While the scrollbar can still scroll further down, keep scrolling
	# and asking for the scroll height to check again
	while (y_position != scroll_height):
		y_position = scroll_height
		web_driver.execute_script(scroll_to_command.format(scroll_height))

		# Page needs to load yet again otherwise the scroll height matches the y position
		# and it breaks out of the loop
		time.sleep(4)
		scroll_height = web_driver.execute_script(get_scroll_height_command)

def create_channel_directory(channel_id):
	# Make new directory to house correlated youtube channel files
	if not os.path.isdir(channel_id):
		os.makedirs(channel_id)

def create_video_ids_list(channel_id, web_driver)
	video_ids_list = []
	print 'Hold up! Creating video ids list first...'

	try:
		urls_already_found = get_previously_parsed_video_ids(channel_id)
		video_ids_list = [video_element.get_attribute('href') + '\n' for video_element in web_driver.find_elements_by_xpath("//*[@id='video-title']") if (video_element.get_attribute('href') + '\n') not in urls_already_found]
		print '{} new videos found for {}.'.format(len(video_ids_list), channel_id)

		return video_ids_list
	except KeyboardInterrupt:
		print '\nStopping! Bye.'
	except Exception as e:
		print e
	finally:
		# Make sure the web driver closes otherwise it keeps hogging RAM
		if web_driver:
			web_driver.close()

def create_video_file(channel_id, video_ids_list):
	# Save off urls into videos file within the channel-specific directory
	with open('{}/{}_videos.txt'.format(channel_id, channel_id), 'a+') as video_file:
		video_file.writelines(video_ids_list)

def initialize_user_page_with_id(channel_id, web_driver)
	# Open the videos page to parse all video urls
	web_driver.get('https://www.youtube.com/user/{}/videos'.format(channel_id))

def initialize_user_page_with_search(channel_id, web_driver)
	# Search for the videos page to parse all video urls
	web_driver.get('https://www.youtube.com/results?search_query={}'.format("+".join(channel_id.split(' '))))
	time.sleep(3)

	# A tenuous solution for now. Try to find the first web element that contains an href populated with a channel url
	# It's best to try and find the exact search query value that will return the channel you want as the first result
	channel_url = web_driver.find_element_by_xpath('//a[contains(@href, \'/channel\')]').get_attribute('href') + '/videos'
	web_driver.get(channel_url)

# Get a complete list of urls that we've already parsed
def get_previously_parsed_video_ids(channel_id):
	url_list = []

	if os.path.exists('{}/{}_videos.txt'.format(channel_id, channel_id)):
		with open('{}/{}_videos.txt'.format(channel_id, channel_id), 'r') as unread_file:
			url_list = unread_file.readlines()

	if os.path.exists('{}/{}_videos_read.txt'.format(channel_id, channel_id)):
		with open('{}/{}_videos_read.txt'.format(channel_id, channel_id), 'r') as read_file:
			url_list += read_file.readlines()

	return url_list

def internet_connection():
	try:
		socket.create_connection(('www.youtube.com', 80), timeout=3)
		return True
	except:
		pass
	return False

# Function can be broken up. Does too many things currently
def open_videos_and_scrape(channel_id, keyword_list, web_driver):
	# -------------- separate function --------------
	url = None
	url_list = []
	# Grab all of the unread video urls we have on file
	with open('{}/{}_videos.txt'.format(channel_id, channel_id), 'r') as url_file:
		url_list = url_file.readlines()
	# -----------------------------------------------

	try:
		while url_list:
			# should break this out into separate function so can parse single video url or loop through a list
			url = url_list.pop()

			if not internet_connection():
				raise Exception('Exception: No internet connection!')

			web_driver.get(url)

			scroll_to_bottom_of_page(web_driver)

			# ----- separate function? -------
			print 'Creating comments list...'
			comments_list = [comment_element.text + '\n\n' for comment_element in web_driver.find_elements_by_xpath("//*[@id='content-text']")]
			# -----------------

			print 'Checking for keywords...'
			saved_comments = []
			for comment in comments_list:
				for keyword in keyword_list:
					# Uncomment this line if you want an explicit check for the keyword, otherwise it acts as a fuzzy search
					# if keyword in [word for word in comment.split(' ')]:
					if keyword in comment:
						saved_comments.append(comment.encode('utf8'))
						break

			# ---------- maybe separate function --------------
			# Save comments to file
			if saved_comments:
				print 'Writing to file!'
				with open('{}/{}_comments.txt'.format(channel_id, channel_id), 'a+') as comment_file:
					comment_file.write(url)
					comment_file.writelines(saved_comments)
					comment_file.write('--------------------------------------------\n\n')
			# ------------------------------

			# separate function ------------
			saved_comments = []
			# Save the new list of urls minus the one we just processed
			with open('{}/{}_videos.txt'.format(channel_id, channel_id), 'w') as updated_url_file:
				updated_url_file.writelines(url_list)
			# ------------------------------

			# separate function ------------
			# Add the processed url to the read file
			with open('{}/{}_videos_read.txt'.format(channel_id, channel_id), 'a+') as read_file:
				read_file.write(url)
			# ------------------------------

			print 'Onto the next url.'
			web_driver.close()
			web_driver = None

	except KeyboardInterrupt:
		print '\nStopping! Bye.'
	except Exception as e:
		print e
	finally:
		# Make sure the web driver closes otherwise it keeps hogging RAM
		if web_driver:
			web_driver.close()

# Do I need this function? Should probably add a main function instead
def scrape_videos(channel_id, keyword_list, web_driver, dynamic_channel):
	create_channel_directory(channel_id)
	web_driver = init_web_driver()

	if dynamic_channel:
		initialize_user_page_with_search(channel_id, web_driver)
	else:
		initialize_user_page_with_id(channel_id, web_driver)

	# The videos page should be open now. Scroll to the bottom of it
	scroll_to_bottom_of_page(web_driver)

	video_ids_list = create_video_ids_list(channel_id, web_driver)
	create_video_file(channel_id, video_ids_list)
	open_videos_and_scrape(channel_id, keyword_list, web_driver)

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-c', '--channel-id', help='The unique channel id to perform actions against.', action='store', dest='channel_id', required=True)
arg_parser.add_argument('-k', '--keywords', help='Double-quoted, comma-separated string of keywords to search for. E.g. "test, test1, test2"', action='store', dest='keywords', default='')
arg_parser.add_argument('-d', '--dynamic-channel', help='Channel has a dynamic id so try to search for it first.', action='store_true', dest='dynamic_channel')
args = vars(arg_parser.parse_args())

channel_id = args.get('channel_id')
keyword_list = [keyword.strip() for keyword in (args.get('keywords')).split(',')]
dynamic_channel = args.get('dynamic_channel')
web_driver = None

if keyword_list:
	scrape_videos(channel_id, keyword_list, web_driver, dynamic_channel)
else:
	print 'No keywords specified...'

print 'Finished.'

