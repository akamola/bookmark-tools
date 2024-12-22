#!/usr/bin/env python3
# coding: utf-8

import csv
import datetime
import sys

# Setup

date = datetime.date.today()
version = '0.1'

# Methods

# Main function
def main():
	print( 'Pocket CSV to bookmark.html ' + version )

	csvpath = read_user_input()
	links = read_csv( csvpath )
	write_html( links )

	print( 'Done' )

# Read Pocket CSV
def read_csv( csvpath ):
	print( 'Read file ' + csvpath + ' ', end='' )

	with open ( csvpath ) as csvfile:
		links = []

		reader = csv.DictReader( csvfile )
		for row in reader:
			link = {
				'title':		row['title'],
				'url':			row['url'],
				'time_added':	row['time_added'],
				'cursor':		row['cursor'],
				'tags':			row['tags'],
				'status':		row['status']
			}
			link = transform_data( link )
			links.append(link)
			print( '.', end='' )

	print(' Done: %i Links' % ( len(links) ) )
	return links

# Read user input from CLI
def read_user_input():
	csvpath = ''

	user_input = sys.argv
	if ( len(user_input) >= 2 ):
		csvpath = user_input[1]

	return csvpath

# Transform Pocket data to bookmark.html compatible data
def transform_data( link ):
	# Transform unread status
	if link['status'] == 'unread':
		link['status'] = 1
	elif link['status'] == 'archive':
		link['status'] = 0
	else:
		link['status'] = 1

	# Transform tags
	link['tags'] = link['tags'].replace('|', ',')

	# Add tag with import date
	tag = 'pocket-%s' % (date)
	if ( len(link['tags']) >= 1 ):
		tag = ',' + tag
	link['tags'] += tag

	return link

# Write bookmark.html file
def write_html( links ):
	filename = 'pocket_%s.html' % (date)
	print( 'Write file %s ' % (filename), end='' )

	with open( filename, 'w' ) as f:
		# Write boomark.html header
		# @see https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/aa753582(v=vs.85)
		f.write( '<!DOCTYPE NETSCAPE-Bookmark-file-1>\n' )
		f.write( '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n' )
		f.write( '<Title>Bookmarks %s</Title>\n' % (date) )
		f.write( '<H1>Bookmarks</H1>\n' )
		f.write( '<DL><p>\n' )
		for row in links:
			f.write( '\t<DT><A HREF="%s" ADD_DATE="%s" PRIVATE="0" TOREAD="%i" TAGS="%s">%s</A></DT>\n' % ( row['url'], row['time_added'], row['status'], row['tags'], row['title'] ) )
			print( '.', end='' )
		f.write( '</DL></p>\n' )
	print('')

# Start

main()
