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

API_KEY = 'AIzaSyC9NdNT6f13uX6zoU_auHy9uXdKqtPqz0w'
YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'


ALL_COMMS = []

class YouTubeApi():

    def load_comments(self, mat):
        for item in mat["items"]:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            ALL_COMMS.append(comment)
            # print("Comment by {}: {}".format(author, text))
            if 'replies' in item.keys():
                for reply in item['replies']['comments']:
                    rauthor = reply['snippet']['authorDisplayName']
                    rtext = reply["snippet"]["textDisplay"]
                    ALL_COMMS.append(reply)

                # print("\n\tReply by {}: {}".format(rauthor, rtext), "\n")

    def get_video_comment(self, video_url, max_results = 100, key = API_KEY):
        # parser = argparse.ArgumentParser()
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
            self.load_comments(mat)

            while nextPageToken:
                parms.update({'pageToken': nextPageToken})
                matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
                mat = json.loads(matches)
                nextPageToken = mat.get("nextPageToken")
                print("\nPage : ", i)
                print("------------------------------------------------------------------")

                self.load_comments(mat)

                i += 1
        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL or Fetch comments at a moment")
        return

    def load_search_res(self, search_response):
        videos, channels, playlists = [], [], []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
              videos.append("{} ({})".format(search_result["snippet"]["title"],
                                         search_result["id"]["videoId"]))
            elif search_result["id"]["kind"] == "youtube#channel":
              channels.append("{} ({})".format(search_result["snippet"]["title"],
                                           search_result["id"]["channelId"]))
            elif search_result["id"]["kind"] == "youtube#playlist":
              playlists.append("{} ({})".format(search_result["snippet"]["title"],
                                search_result["id"]["playlistId"]))

        print("Videos:\n", "\n".join(videos), "\n")
        print("Channels:\n", "\n".join(channels), "\n")
        print("Playlists:\n", "\n".join(playlists), "\n")

    def search_keyword(self):
        # parser = argparse.ArgumentParser()
        mxRes = 20
        # parser.add_argument("--s", help="calls the search by keyword function", action='store_true')
        # parser.add_argument("--r", help="define country code for search results for specific country", default="IN")
        # parser.add_argument("--search", help="Search Term", default="Srce Cde")
        # parser.add_argument("--max", help="number of results to return")
        # parser.add_argument("--key", help="Required API key")
        #
        # args = parser.parse_args()

        if not args.max:
            args.max = mxRes

        if not args.key:
            exit("Please specify API key using the --key= parameter.")

        parms = {
                    'q': args.search,
                    'part': 'id,snippet',
                    'maxResults': args.max,
                    'regionCode': args.r,
                    'key': args.key
                }

        try:
            matches = self.openURL(YOUTUBE_SEARCH_URL, parms)

            search_response = json.loads(matches)
            i = 2

            nextPageToken = search_response.get("nextPageToken")

            print("\nPage : 1 --- Region : {}".format(args.r))
            print("------------------------------------------------------------------")
            self.load_search_res(search_response)

            while nextPageToken:
                parms.update({'pageToken': nextPageToken})
                matches = self.openURL(YOUTUBE_SEARCH_URL, parms)

                search_response = json.loads(matches)
                nextPageToken = search_response.get("nextPageToken")
                print("Page : {} --- Region : {}".format(i, args.r))
                print("------------------------------------------------------------------")

                self.load_search_res(search_response)

                i += 1

        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL or Fetch comments at a moment")

    def load_channel_vid(self, search_response):
        videos = []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append("{} ({})".format(search_result["snippet"]["title"],
                                         search_result["id"]["videoId"]))

        print("###Videos:###\n", "\n".join(videos), "\n")

    def channel_videos(self):
        parser = argparse.ArgumentParser()
        mxRes = 20
        parser.add_argument("--sc", help="calls the search by channel by keyword function", action='store_true')
        parser.add_argument("--channelid", help="Search Term", default="Srce Cde")
        parser.add_argument("--max", help="number of results to return")
        parser.add_argument("--key", help="Required API key")

        args = parser.parse_args()

        if not args.max:
            args.max = mxRes

        if not args.channelid:
            exit("Please specify channelid using the --channelid= parameter.")

        if not args.key:
            exit("Please specify API key using the --key= parameter.")

        parms = {
                   'part': 'id,snippet',
                   'channelId': args.channelid,
                   'maxResults': args.max,
                   'key': args.key
               }

        try:
            matches = self.openURL(YOUTUBE_SEARCH_URL, parms)

            search_response = json.loads(matches)

            i = 2

            nextPageToken = search_response.get("nextPageToken")
            print("\nPage : 1")
            print("------------------------------------------------------------------")

            self.load_channel_vid(search_response)

            while nextPageToken:
                    parms.update({'pageToken': nextPageToken})
                    matches = self.openURL(YOUTUBE_SEARCH_URL, parms)

                    search_response = json.loads(matches)
                    nextPageToken = search_response.get("nextPageToken")
                    print("Page : ", i)
                    print("------------------------------------------------------------------")

                    self.load_channel_vid(search_response)

                    i += 1

        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL or Fetch comments at a moment")

    def openURL(self, url, parms):
            f = urlopen(url + '?' + urlencode(parms))
            data = f.read()
            f.close()
            matches = data.decode("utf-8")
            return matches


def main():
    y = YouTubeApi()
    y.get_video_comment("gfr44G1KJmc")
    # if str(sys.argv[1]) == "--s":
    #     y.search_keyword()
    # elif str(sys.argv[1]) == "--c":
    #     y.get_video_comment()
    # elif str(sys.argv[1]) == "--sc":
    #     y.channel_videos()
    # else:
    #     print("Invalid Arguments\nAdd --s for searching video by keyword after the filename\nAdd --c to list comments after the filename\nAdd --sc to list vidoes based on channel id")
    pickle.dump(ALL_COMMS, open("all_the_stuff.pkl","wb"))

if __name__ == '__main__':
    # main()
    import os
    import numpy as np
    import pandas as pd
    cwd = '/home/dimtsi/Dropbox/UvA/2nd Semester/Big Data/Project/src/youtube_tutorial/python-youtube-api'
    os.chdir(cwd)
    with open('all_the_stuff.pkl', 'rb') as pickle_file:
        all_comms = pickle.load(pickle_file)
    len(all_comms)
    df = pd.DataFrame(all_comms)

    pd.DataFrame(list(df['snippet']))['textDisplay']
    for comm in (all_comms[:150]):
        print(comm['snippet']['textDisplay'])

