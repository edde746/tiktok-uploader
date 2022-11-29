import requests

USER_AGENT = 'YetAnotherContentThief by /u/edde74635'

def get_posts(subreddit='shitposting', time='week', limit=10, after=None):
    url = 'https://www.reddit.com/r/%s/top.json?t=%s&limit=%s&after=%s' % (subreddit, time, limit, after)
    r = requests.get(url, headers={'User-Agent': USER_AGENT})
    if r.status_code == 200:
        # filter out stickied posts and nsfw posts
        json = r.json()
        json['data']['children'] = [post for post in json['data']['children'] if not post['data']['stickied'] and not post['data']['over_18']]
        return json
    else:
        return None

def download_images(json):
    for post in json['data']['children']:
        url = post['data']['url']
        filename = url.split('/')[-1]
        r = requests.get(url, headers={'User-Agent': USER_AGENT})
        if r.status_code == 200:
            with open('to_upload/%s' % filename, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
