import twitter
import os

class TwitterBot(object):

    def __init__(self, consumer_key, consumer_secret,
                 access_key, access_secret,
                 source_file_name):
        self.source_file_name = source_file_name
        self.twitter = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                      access_token_key=access_key, access_token_secret=access_secret,
                      input_encoding=None)

    def _get_current_file(self):
        with open(self.source_file_name) as source_fh:
            data = source_fh.read()
            return data

    def post(self):
        status_str = self._get_current_file()
        try:
          self.twitter.PostUpdate(status_str)
        except:
          raise

if __name__ == '__main__':

    bot = TwitterBot(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'],
                       os.environ['ACCESS_KEY'], os.environ['ACCESS_SECRET'],
                      'r_all_rising.what')

    bot.post()