import pandas as pd

def calculate_statistics(aggregated_data):
    """Calculate and display statistics for processed comments"""
    if not aggregated_data:
        print("No comments to analyze.")
        return

    try:
        # Convert to DataFrame
        df = pd.DataFrame(aggregated_data)

        # Basic counts
        total_comments = len(df)
        positive_count = len(df[df['sentiment'] == 'positive'])
        negative_count = len(df[df['sentiment'] == 'negative'])
        neutral_count = len(df[df['sentiment'] == 'neutral'])

        # Calculate percentages
        pos_percent = (positive_count / total_comments) * 100
        neg_percent = (negative_count / total_comments) * 100
        neu_percent = (neutral_count / total_comments) * 100

        # Print statistics
        print("\nSentiment Analysis Statistics:")
        print("-" * 30)
        print(f"Total Comments Analyzed: {total_comments}")
        print(f"Positive Comments: {positive_count} ({pos_percent:.1f}%)")
        print(f"Negative Comments: {negative_count} ({neg_percent:.1f}%)")
        print(f"Neutral Comments: {neutral_count} ({neu_percent:.1f}%)")

        if not df.empty:
            print("\nMost Extreme Comments:")
            print("-" * 30)
            most_positive = df.loc[df['compound'].idxmax()]
            most_negative = df.loc[df['compound'].idxmin()]
            
            print(f"\nMost Positive (score: {most_positive['compound']:.2f}):")
            print(f"{most_positive['text'][:100]}...")
            print(f"\nMost Negative (score: {most_negative['compound']:.2f}):")
            print(f"{most_negative['text'][:100]}...")

    except Exception as e:
        print(f"Error calculating statistics: {e}")