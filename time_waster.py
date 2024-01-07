import argparse
import os
import pandas as pd
import random
import requests
from datetime import datetime

class RedditScraper:
   def __init__(self, subreddit, min_score=5, min_num_comments=20):
       self.all_posts = pd.DataFrame()
       self.headers = {'User-agent': 'Mozilla/5.0'}
       self.min_num_comments = min_num_comments
       self.min_score = min_score
       self.params = {"limit": 100}
       self.subreddit = subreddit
       self.url = f"https://www.reddit.com/r/{self.subreddit}.json"

   def make_subsequent_reddit_requests(self, last_post_id):
       self.params["after"] = last_post_id
       response = requests.get(self.url, headers=self.headers, params=self.params)
       data = response.json()
       last_post_id = data['data']['children'][-1]['data']['name']
       return response, last_post_id

   def get_posts(self, response):
       return pd.DataFrame([x['data'] for x in response.json()['data']['children']])

   def get_select_posts(self, all_posts):
       all_posts["created_at"] = all_posts.created_utc.apply(lambda x: datetime.utcfromtimestamp(x)).dt.date
       min_date = all_posts.created_at.min().strftime("%Y-%m-%d")
       all_posts.drop(columns=['created_utc'], inplace=True)
       all_posts = all_posts.drop_duplicates(subset=['url'])
       select = all_posts[(all_posts.score > self.min_score) & (all_posts.num_comments > self.min_num_comments) & ~all_posts.url.str.contains("jpg|jpeg")][['subreddit', 'title','url','num_comments','score', 'created_at']]

       filename_select = f'select_{self.subreddit}_{min_date}.csv'
       select.to_csv(filename_select, index=False)
       print(f"Number of selected posts: {len(select)}, Saved as: {filename_select}")


   def get_new_posts(self):
       response = requests.get(self.url, headers=self.headers, params=self.params)
       data = response.json()
       last_post_id = data['data']['children'][-1]['data']['name']
       for i in range(20):
           try:
               response, last_post_id = self.make_subsequent_reddit_requests(last_post_id)
               temp_df = self.get_posts(response)
               self.all_posts = pd.concat([self.all_posts, temp_df])
               print(len(self.all_posts), last_post_id)
           except:
               print("max posts reached")
               break
       print("Length all_posts: ", len(self.all_posts))
       if len(self.all_posts) > 0:
           self.get_select_posts(self.all_posts)

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Generate a new link.')
   parser.add_argument('--new_subreddit', type=str, help='Generate posts for a subreddit')
   parser.add_argument('--min_score', type=int, help='Minimum score')
   parser.add_argument('--min_num_comments', type=int, help='Minimum number of comments')

   parser.add_argument('--random_link', type=str, help='Generate a random new link')
   parser.add_argument('--list_options', action='store_true')
   
   args = parser.parse_args()
   
   if args.new_subreddit:
       min_score = args.min_score or 5
       min_num_comments = args.min_num_comments or 20
       scraper = RedditScraper(args.new_subreddit, min_score, min_num_comments)
       scraper.get_new_posts()
       
   if args.random_link:
       # Find file
       subreddit_name = lower(args.random_link)
       relevant_files = [file for file in os.listdir() if file.endswith('csv') and "select" in file and subreddit_name in file]
       largest_file = max(relevant_files, key=os.path.getsize)
       df = pd.read_csv(largest_file)

       # Get random link
       urls_to_choose_from = df.url.to_list()
       random_url = random.choice(urls_to_choose_from)
       print(random_url)
       
   if args.list_options:
       relevant_files = [file.lower() for file in os.listdir() if file.endswith('csv') and "select" in file]
       for file in relevant_files:
           fmt = file.split("select_")[1].replace("_", "").replace(".csv","")
           print(fmt)
