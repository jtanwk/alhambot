# What's your name, man?
## My name is Alexander Hamilton

https://twitter.com/mynameisa15n

_Edit: Jan 4, 2019. The bot has been suspended by Twitter, and it's remarkably difficult to find out why specifically. My guess is that it's bad form to quote complete strangers' tweets who aren't following the bot's account. This project is on hold until a sustainable way forward is determined._

This project is a Twitter bot that identifies and retweets tweets that match the syllable structure and stress pattern of Lin-Manuel Miranda's introductory line in the eponymous Broadway musical, *Alexander Hamilton*.

I'm attempting a few things for the first time here, including:
- Writing a Twitter bot with Tweepy
- Writing a new Class (!) in a side project
- Building an app on Heroku
- Using [CMU's Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) to count syllables and identify stress patterns

The primary inspiration for this project (outside of recently watching the musical for the first time) is the [Deck the Halls twitter bot](https://twitter.com/falalala_la). Thanks also to the fairly detailed guides that I used for different aspects of this project:
- [Wale Adesina](https://scotch.io/tutorials/build-a-tweet-bot-with-python) for guidance on the overall structure of the bot.
- [Brian Caffrey](https://briancaffey.github.io/2016/04/05/twitter-bot-tutorial.html) for how to deploy the bot via Heroku.
- [Emily Cain](https://dev.to/emcain/how-to-set-up-a-twitter-bot-with-python-and-heroku-1n39) for the critical portion on how to use environment variables in Heroku for Twitter OAuth instead of publishing all of my tokens online.

# How It Works

## What it looks for

The script catches tweets that can be sung in place of the name "Alexander Hamilton" and retweets them accordingly. To me, that means the phrase has to match two main criteria:
1. Has 7 syllables
2. Words must be stressed on the first and fifth syllables to match the onset of the words (AH-lexander HA-milton).

I did originally consider also making sure the tweets matched the onset sounds (i.e. first syllable starting with 'A', fifth syllable starting with 'H') but an early trial of the bot showed incredibly few tweets matching this. Phrases not matching this have also been shown to work fairly well (e.g. per [this Reddit post](https://www.reddit.com/r/hamiltonmusical/comments/5bjib6/whats_your_name_man/)).

## Data source

It turns out that computationally calculating the number of syllables from an English word is perilous at best. [This Quora thread](https://www.quora.com/Is-there-an-authoritative-resource-or-algorithm-that-defines-the-number-of-syllables-in-an-English-word) summarizes the process better than I can reproduce it here.

So - rather than do it algorithmically, I'm using [CMU's Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) to count syllables and identify stress patterns. One advantage is it provides not only segmented syllables and onset sounds but also indications of _where the stress falls in a word or phrase_, which further helps me match any given phrase to "Alexander Hamilton". One major weakness of using a static dictionary is, of course, being unable to consider words not already in the dictionary. I suppose it's better than guessing.

## Counting syllables and stresses

The lexical stress pattern in "Alexander Hamilton" can be very roughly represented as "2010100", where 1s are primary stresses, 2s are secondary stresses, and 0s indicate no stress. (While this might be tough to explain in text on a screen, just listen to the [soundtrack](https://www.youtube.com/watch?v=VhinPd5RRJw) - it leaps right out at you.)

![From CMU's Pronouncing Dictionary](https://raw.githubusercontent.com/jtanwk/alhambot/master/images/img1.png?raw=true)

I've relaxed this somewhat for the Twitter bot. After some rudimentary cleaning (it strips out all non-alphanumeric characters with regex), it looks for phrases that:
- Have 7 syllables in total
- Have either primary or secondary stresses on the 1st, 3rd, and 5th syllables such that all of the following are acceptable: 1010100, 2010100, 2010102, and so on
- Tweets with words that aren't found in CMU's Pronouncing Dictionary (and for which we can't count syllables) are excluded

And that's it! Once the bot notices a tweet that matches those criteria, it'll retweet it like so:

![](https://raw.githubusercontent.com/jtanwk/alhambot/master/images/img2.png?raw=true)

# What's next?

Potential refinements and/or extensions that are way outside my current abilities:
- Refining the criterion that make a phrase sound like another phrase (e.g. incorporating Jaro-Winkler scores or Levenshtein distance as comparison metrics). This requires a deeper and more technical knowledge of computational linguistics that I currently have.
- Actually calculating syllables by algorithm rather than with a dictionary. Maybe a good NLP machine learning problem?
- Extend syllable counting to non-word words (e.g. the "II" in "Boyz II Men" is ideally parsed as one syllable).
- Expand phrase identification beyond the text in tweets to look at *words in images* attached to tweets. Requires some knowledge of computer vision and a text extractor program. (Just you wait, just you wait...)
