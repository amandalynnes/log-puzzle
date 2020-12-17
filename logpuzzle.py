#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
__author__ = "Amanda Simmons, Piero M, Pete M, Kano M"

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    with open(filename, 'r') as f:
        # file_contents = f.readlines()
        list_of_tups = []
        split_website = filename.split('_')
        filename_base = f'http://{split_website[1]}'
        for line in f:
            pattern = r"GET\s(.*/\w-(\w+).\w+)"
            match_obj = re.search(pattern, line)
            if match_obj:
                url = match_obj.group(1)
                file_name_end = match_obj.group(2)
                file_end_url_tup = (file_name_end, url)
                list_of_tups.append(file_end_url_tup)
                # print(url)
                # print(file_name_end)
        set_of_tups = set(list_of_tups)
        sorted_list_of_tups = sorted(set_of_tups)
        # print(sorted_list_of_tups)
        # print(set_of_tups)
        alpha_sorted_urls = [filename_base + tup[1] for tup in sorted_list_of_tups]
        return alpha_sorted_urls

def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    os.makedirs(dest_dir)
    with open(f'{dest_dir}/index.html', 'a') as f:
        f.write('<html>\n<body>')
    for index, img_url in enumerate(img_urls):
        print(f'Retrieving {img_url} at index:{index}')
        local_filename, headers = urllib.request.urlretrieve(img_url, f'{dest_dir}/img{index}')
        with open(f'{dest_dir}/index.html', 'a') as f:
            f.write(f'<img src="img{index}">')
    with open(f'{dest_dir}/index.html', 'a') as f:
        f.write('</body>\n</html>')


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
