# reddit.com/r/all/rising Twitter Bot
[Scrapy](https://scrapy.org/) spider that scrapes Reddit [/r/all/rising](https://www.reddit.com/r/all/rising/) for sub distribution and bot that posts to Twitter every hour using [python-twttier](https://github.com/bear/python-twitter). You can see it in action [here.](https://twitter.com/r_all_risingBot/)  

Set up to run on Heroku, just set up your config vars `CONSUMER_KEY CONSUMER_SECRET ACCESS_TOKEN ACCESS_SECRET` from Twitter. You may need to change the permissions of script.sh by executing `chmod u+x script.sh`

For educational purposes only.