from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

def analyze_with_vader(text):
    """
    Analyze text sentiment using VADER
    Returns: dictionary of scores and sentiment label
    """
    # Create VADER analyzer
    analyzer = SentimentIntensityAnalyzer()
    
    # Get sentiment scores
    scores = analyzer.polarity_scores(text)
    
    # Determine sentiment label based on compound score
    if scores['compound'] >= 0.05:
        sentiment = 'positive'
    elif scores['compound'] <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return {
        'text': text,
        'compound': scores['compound'],
        'pos': scores['pos'],
        'neu': scores['neu'],
        'neg': scores['neg'],
        'sentiment': sentiment
    }

sentences = ["VADER is smart, handsome, and funny.",  # positive sentence example
             "VADER is smart, handsome, and funny!",  # punctuation emphasis handled correctly (sentiment intensity adjusted)
             "VADER is very smart, handsome, and funny.", # booster words handled correctly (sentiment intensity adjusted)
             "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
             "VADER is VERY SMART, handsome, and FUNNY!!!", # combination of signals - VADER appropriately adjusts intensity
             "VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!", # booster words & punctuation make this close to ceiling for score
             "VADER is not smart, handsome, nor funny.",  # negation sentence example
             "The book was good.",  # positive sentence
             "At least it isn't a horrible book.",  # negated negative sentence with contraction
             "The book was only kind of good.", # qualified positive sentence is handled correctly (intensity adjusted)
             "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
             "Today SUX!",  # negative slang with capitalization emphasis
             "Today only kinda sux! But I'll get by, lol", # mixed sentiment example with slang and constrastive conjunction "but"
             "Make sure you :) or :D today!",  # emoticons handled
             "Catch utf-8 emoji such as such as 💘 and 💋 and 😁",  # emojis handled
             "Not bad at all"  # Capitalized negation
             ]

results = []
for sentence in sentences:
    results.append(analyze_with_vader(sentence))

df = pd.DataFrame(results)

print("\nDetailed Sentiment Analysis Results:")
print(df[['text', 'compound', 'pos', 'neu', 'neg', 'sentiment']])

# Summary statistics
print("\nSummary Statistics:")
print(f"Average Compound Score: {df['compound'].mean():.3f}")
print(f"Number of Positive Texts: {len(df[df['sentiment'] == 'positive'])}")
print(f"Number of Negative Texts: {len(df[df['sentiment'] == 'negative'])}")
print(f"Number of Neutral Texts: {len(df[df['sentiment'] == 'neutral'])}")

# Most extreme sentiments
print("\nMost Positive Text:")
print(df.loc[df['compound'].idxmax()]['text'])
print(f"Compound Score: {df['compound'].max():.3f}")

print("\nMost Negative Text:")
print(df.loc[df['compound'].idxmin()]['text'])
print(f"Compound Score: {df['compound'].min():.3f}")








#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
# Download a dataset like "Amazon Reviews" or "Twitter Sentiment Dataset" from Kaggle
#df = pd.read_csv('your_dataset.csv')
#texts = df['review_text'].tolist()  # column name depends on your dataset



#while True:
    # Get input from user
#    text = input("\nEnter text to analyze (or 'quit' to exit): ")
    
   # Check if user wants to quit
#    if text.lower() == 'quit':
#        break