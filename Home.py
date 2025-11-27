import pandas as pd

url = "https://www.dropbox.com/s/wx0fsu580mfl0kjcaub2f/cleaned_reviews.csv?dl=1"

df = pd.read_csv(url)
print(df.columns.tolist())
