from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score
import numpy as np

TWSS = 'twss_joke'
REG = 'regular'

SOURCES = [
    ('data/twsss.txt', TWSS),
    ('data/twst.txt', TWSS),
    ('data/twss-office.txt', TWSS),
    # ('data/gr.txt', REG),
    ('data/fml.txt', REG)
]

def readFile(path):
    f = open(path, 'r')
    return f.read().split('\n')

def buildDataFrame(path, classification):
    rows = []
    index = []
    for i, entry in enumerate(readFile(path)):
        rows.append({'text': entry, 'class': classification})
        index.append(path + str(i))
 
    dataFrame = DataFrame(rows, index=index)
    return dataFrame


data = DataFrame({'text': [], 'class': []})
for path, classification in SOURCES:
    data = data.append(buildDataFrame(path, classification))

# data = data.reindex(np.random.permutation(data.index))
pipeline = Pipeline([
    ('vectorizer',  CountVectorizer()),
    ('classifier',  MultinomialNB()) ])

examples = ['how big is it', 'put it in here', 'how is that even a joke']

k_fold = KFold(n=len(data), n_folds=6)
scores = []
confusion = np.array([[0, 0], [0, 0]])
for train_indices, test_indices in k_fold:
    train_text = data.iloc[train_indices]['text'].values
    train_y = data.iloc[train_indices]['class'].values

    test_text = data.iloc[test_indices]['text'].values
    test_y = data.iloc[test_indices]['class'].values

    pipeline.fit(train_text, train_y)
    predictions = pipeline.predict(test_text)

    confusion += confusion_matrix(test_y, predictions)
    score = f1_score(test_y, predictions, pos_label=TWSS)
    scores.append(score)

print('Total entries classified:', len(data))
print('Score:', sum(scores)/len(scores))
print('Confusion matrix:')
print(confusion)
print(pipeline.predict(examples))