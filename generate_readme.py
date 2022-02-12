#!/usr/bin/env python
import string
import feedparser
from io import TextIOWrapper
from tqdm import tqdm
import listparser


def parse_opml():
	rs = {}
	feeds = listparser.parse(open('feeds.opml').read()).feeds
	for feed in feeds:
		if len(feed['categories']) == 0:
			continue
		category = feed['categories'][0][0]
		if not category in rs:
			rs[category] = []
		rs[category].append(feed)
	return rs

def write_header(writer: TextIOWrapper):
	with open('header.tmpl') as f:
		content = f.read()
		writer.write(content)
def write_footer(writer: TextIOWrapper):
	with open('footer.tmpl') as f:
		writer.write(f.read())

def get_feed_link(feed_url: string):
	try:
		info = feedparser.parse(feed_url)
		if 'feed' in info and 'link' in info['feed']:
			return info['feed']['link']
	except:
		return None

def write_body(writer: TextIOWrapper):
	feeds = parse_opml()
	categories = feeds.keys()
	num_feeds = 0
	for category in categories:

		print('- Category: {}'.format(category))
		writer.write('\n\n### {}\n'.format(category))
		category_feeds = feeds[category]
		for feed in tqdm(category_feeds):
			feed_url = feed['url']
			feed_title = feed['title']
			link = get_feed_link(feed_url)
			if link:
				writer.write('\n- [{}]({})\n```\n{}\n```'.format(feed_title, link, feed_url))
			else:
				writer.write('\n- {}\n```\n{}\n```'.format(feed_title, feed_url))
			num_feeds += 1
	print('Number of rss feeds: {}'.format(num_feeds))

def generate_readme():
	with open('README.md', 'w') as writer:
		write_header(writer)
		write_body(writer)
		write_footer(writer)


if __name__ == '__main__':
	generate_readme()