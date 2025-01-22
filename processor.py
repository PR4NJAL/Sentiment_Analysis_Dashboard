from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
comments_data = []
def processor(valid_comment):
    try:
        text = valid_comment['text']
        score = analyzer.polarity_scores(text)

        if score['compound'] >= 0.05:
            sentiment = 'positive'
        elif score['compound'] <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return {
            'text': text,
            'score': score,
            'compound': score['compound'],
        #'pos': score['pos'],
        #'neu': score['neu'],
        #'neg': score['neg'],
            'sentiment': sentiment
        }
    except Exception as e:
        print('Error processing comment:', e)
        return None
    