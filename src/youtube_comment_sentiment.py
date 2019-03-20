"""
-*- coding: utf-8 -*-
========================
Python YouTube API
========================

Forked from: Chirag Rathod
https://github.com/srcecde/python-youtube-api/blob/master/youtube_api_cmd.py

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

from nltk.sentiment.vader import SentimentIntensityAnalyzer as sid


API_KEY = 'AIzaSyC9NdNT6f13uX6zoU_auHy9uXdKqtPqz0w'
YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'



class YouTubeApi():
    all_comments = []

    def get_single_comment_info(self, comment):
        text = comment["snippet"]["textDisplay"]
        likeCount = comment["snippet"]["likeCount"]
        date = comment["snippet"]["publishedAt"]
        return {'text' : text, 'likeCount': likeCount, 'date' : date}

    def load_comments(self, mat):
        comments = []
        for item in mat["items"]:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            self.all_comments.append(self.get_single_comment_info(comment))
            # self.all_comments.append(comment)
            # print("Comment by {}: {}".format(author, text))
            if 'replies' in item.keys():
                for reply in item['replies']['comments']:
                    rauthor = reply['snippet']['authorDisplayName']
                    rtext = reply["snippet"]["textDisplay"]
                    # comment_data = {}
                    info = self.get_single_comment_info(reply)
                    self.all_comments.append(info)
                    # self.all_comments.append(reply)

        # return comments

                # print("\n\tReply by {}: {}".format(rauthor, rtext), "\n")
    # def get_statistics_views(self, video_id, key = API_KEY):
    #     response = youtube.videos().list(
    #     part='statistics, snippet',
    #     id=video_id).execute()
    #
    #     view_count = response['items'][0]['statistics']['viewCount']
    #     like_count = response['items'][0]['statistics']['likeCount']
    #     dislike_count = response['items'][0]['statistics']['dislikeCount']
    #     return view_count,like_count,dislike_count

    def get_video_comment(self, video_url, max_results = 100, key = API_KEY):
        # parser = argparse.ArgumentParser()
        all_coments = []
        mxRes = 20
        vid = str()

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
            # print("\nPage : 1")
            # print("------------------------------------------------------------------")
            info = self.load_comments(mat)
            if info is not None:
                self.all_comments.append(info)
            # self.all_comments.append()

            while nextPageToken:
                parms.update({'pageToken': nextPageToken})
                matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
                mat = json.loads(matches)
                nextPageToken = mat.get("nextPageToken")
                # print("\nPage : ", i)
                # print("------------------------------------------------------------------")
                comments = self.load_comments(mat)
                if comments is not None:
                    self.all_comments.append(comments)
                i += 1
                if i > 1: #comment_page_limit
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


def extract_comments():
    data = []
    y = YouTubeApi()
    video_ids = ['8hP9D6kZseM', '6ZfuNTqbHE8', 'GokKUqLcvD8']
    for video_id in video_ids:
        comments = y.get_video_comment(video_id)
        data.append(comments)
    # jsonData=json.dumps(data)
    # with open('data.json', 'a') as outfile:
    #     json.dump(data, outfile)
    return data

def perform_sentiment_analysis(*)
# def obtain_info_single_comment(comment):


    # video_data = pd.read_csv('movies.csv')
    # video_data

    # pickle.dump(ALL_COMMS, open("all_the_stuff.pkl","wb"))

if __name__ == '__main__':
    import os
    import numpy as np
    cwd = '/home/dimtsi/Dropbox/UvA/2nd Semester/Big Data/Project/src'
    os.chdir(cwd)

    data = extract_comments()
    dfs = [pd.DataFrame(data[x]) for x in range(len(data))]
    df = pd.concat(dfs)
    df.columns
    # with open(r"data.json", "r") as read_file:
    #     data = json.load(read_file)
    # pd.DataFrame.from_dict(data[0].values()['snippet'])
    from nltk.sentiment.vader import SentimentIntensityAnalyzer as sid
    sid = sid()
    df['sentiment_score'] = df['text'].map(
                lambda comm:sid.polarity_scores(comm)['compound'])
    df.head(50)
    # data.keys()
    # with open('all_the_stuff.pkl', 'rb') as pickle_file:
    #     all_comms = pickle.load(pickle_file)
    # df = pd.DataFrame(all_comms)
    #
    # pd.DataFrame(list(df['snippet']))['textDisplay']
    # for comm in (all_comms[:150]):
    #     print(comm['snippet']['textDisplay'])
