"""
-*- coding: utf-8 -*-
========================
Python YouTube API
========================

Developed by: Chirag Rathod (Srce Cde)
Email: chiragr83@gmail.com

========================
"""
import pickle
import json
import sys
from urllib import *
import argparse
from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import  urlopen
import json
import pandas as pd


API_KEY = 'AIzaSyC9NdNT6f13uX6zoU_auHy9uXdKqtPqz0w'
YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'



class YouTubeApi():
    self.all_comments = []

    def load_comments(self, mat):
        comments = []
        for item in mat["items"]:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            self.all_comments.append(comment)
            # print("Comment by {}: {}".format(author, text))
            if 'replies' in item.keys():
                for reply in item['replies']['comments']:
                    rauthor = reply['snippet']['authorDisplayName']
                    rtext = reply["snippet"]["textDisplay"]
                    self.all_comments.append(reply)
        # return comments

                # print("\n\tReply by {}: {}".format(rauthor, rtext), "\n")

    def get_video_comment(self, video_url, max_results = 100, key = API_KEY):
        # parser = argparse.ArgumentParser()
        all_coments = []
        mxRes = 20
        vid = str()
        # parser.add_argument("--c", help="calls comment function by keyword function", action='store_true')
        # parser.add_argument("--max", help="number of comments to return")
        # parser.add_argument("--videourl", help="Required URL for which comments to return")
        # parser.add_argument("--key", help="Required API key")

        # args = parser.parse_args()

        # if not args.videourl:
        #     exit("Please specify video URL using the --videourl=parameter.")
        #
        # if not args.key:
        #     exit("Please specify API key using the --key=parameter.")

        # try:
        #     video_id = urlparse(str(video_url))
        #     print(video_id)
        #     q = parse_qs(video_id.query)
        #     vid = q["v"][0]
        #
        # except:
        #     print("Invalid YouTube URL")

        parms = {
                    'part': 'snippet,replies',
                    'maxResults': max_results,
                    'videoId': video_url,
                    'textFormat': 'plainText',
                    'key': key
                }

        try:

            matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
            i = 2
            mat = json.loads(matches)
            nextPageToken = mat.get("nextPageToken")
            print("\nPage : 1")
            print("------------------------------------------------------------------")
            self.all_comments.append(self.load_comments(mat))

            while nextPageToken:
                parms.update({'pageToken': nextPageToken})
                matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
                mat = json.loads(matches)
                nextPageToken = mat.get("nextPageToken")
                print("\nPage : ", i)
                print("------------------------------------------------------------------")

                self.all_comments.append(self.load_comments(mat))

                i += 1
                if i > 15:
                    break
        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL or Fetch comments at a moment")
        return self.all_comments


    def openURL(self, url, parms):
            f = urlopen(url + '?' + urlencode(parms))
            data = f.read()
            f.close()
            matches = data.decode("utf-8")
            return matches


def main():
    y = YouTubeApi()
    video_ids = ['8hP9D6kZseM', '6ZfuNTqbHE8', 'GokKUqLcvD8']
    for video_id in video_ids:
        comments = y.get_video_comment(video_id)
        with open('data.json', 'a') as outfile:
            json.dump({video_id: comments}, outfile)

    # video_data = pd.read_csv('movies.csv')
    # video_data

    # pickle.dump(ALL_COMMS, open("all_the_stuff.pkl","wb"))

if __name__ == '__main__':
    import os
    import numpy as np
    cwd = '/home/dimtsi/Dropbox/UvA/2nd Semester/Big Data/Project/src'
    os.chdir(cwd)
    main()
    # video_data.head()



    # with open('all_the_stuff.pkl', 'rb') as pickle_file:
    #     all_comms = pickle.load(pickle_file)
    # df = pd.DataFrame(all_comms)
    #
    # pd.DataFrame(list(df['snippet']))['textDisplay']
    # for comm in (all_comms[:150]):
    #     print(comm['snippet']['textDisplay'])
