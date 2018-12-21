# alhambot.py

import tweepy
import re
from os import environ

# Setup syllable counter dictionary
filename = 'cmudict-0.7b.txt'
syllable_dict = {}

# Initialize dictionary
for line in open(filename, encoding='latin-1'):

    if line[0] == ';':
        continue
    else:
        word, entry = line.split('  ')
        syllable_dict[word] = re.sub(r'[^0-9]', '', entry)

# Create function to take a string and count all syllables across words
def matches_al_ham(text):
    '''Returns True if provided string input matches syllable count and stress
    pattern for "Alexander Hamilton" phrase.'''

    def get_syllables(word):
        '''Checks input word against syllable dictionary and returns the number
        of syllables in the word. If the word is not in the dictionary, raises
        a KeyError.'''

        if word.upper() in syllable_dict.keys():
            return re.sub(r'[^0-9]', '', syllable_dict[word.upper()])
        else:
            raise KeyError('Word is not recognized')

    def get_structure(text):
        '''Returns True if text has 7 syllables, and stresses are on 1st and 5th
        syllables.'''

        # Remove all non-alphanumeric and non-space characters
        text = re.sub(r'[^0-9a-zA-Z ]', '', text)

        # Check if 1st, 3rd and 5th syllables are primary or secondary stresses
        pattern = ''.join(list(map(get_syllables, text.split(' '))))

        if len(pattern) != 7:
            return False
        else:
            on_stresses = all([int(pattern[0]) > 0, int(pattern[2]) > 0,
                              int(pattern[4]) > 0])
            # off_stresses = all([int(pattern[1] == 0), int(pattern[3]) == 0,
            #                     int(pattern[5]) == 0])
            return on_stresses and text[0].upper() == 'A' # and off_stresses

    return get_structure(text)

# Create OAuthHander and API instances
CONSUMER_KEY = environ['consumer_key']
CONSUMER_SECRET = environ['consumer_secret']
ACCESS_TOKEN = environ['access_token']
ACCESS_SECRET = environ['access_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

class BotStreamer(tweepy.StreamListener):

    def on_status(self, status):
        '''Overloads existing on_status function.'''
        username = status.user.screen_name
        status_id = status.id
        status_text = status.text

        try:
            if matches_al_ham(status_text):
                print('\nsuccess! retweeting:', status_text)
                message = 'My name is \n' + f'https://twitter.com/{username}/status/{status_id}'
                api.update_status(message)
            else:
                pass
        except KeyError:
            pass

    def on_error(self, status_code):
        '''Disconnect in the case of too many failures in a short period'''
        if status_code == 420:
            return False

# Create new Stream instance
myStreamListener = BotStreamer()
stream = tweepy.Stream(auth=auth, listener=myStreamListener)
stream.filter(languages=['en'], locations=[-180,-90,180,90])
