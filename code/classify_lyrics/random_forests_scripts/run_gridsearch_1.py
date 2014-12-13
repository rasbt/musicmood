# Sebastian Raschka 2014

import pandas as pd
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import EnglishStemmer
import pickle
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from mlxtend.sklearn import DenseTransformer


## Read trainings data

df_train = pd.read_csv('./dataset/training/train_lyrics_1000.csv')
df_test = pd.read_csv('./dataset/training/train_lyrics_1000.csv')

X_train = df_train['lyrics']
y_train = df_train['mood']

X_test = df_test['lyrics']
y_test = df_test['mood']



X_train_feat = vect.fit_transform(X_train, y_train)
X_train_feat = X_train_feat.toarray()

### Label Encoder

pickle_in = open('./label_encoder.p', 'rb')
le = pickle.load(pickle_in)
pickle_in.close()

### Stop words and stemmer

stop_words = pickle.load(open('./stopwords.p', 'rb'))
semantic_words = pickle.load(open('./whitelist_dicts/semantic_words_py34.p', 'rb'))
porter = PorterStemmer()
snowball = EnglishStemmer()

### Tokenizer

tokenizer = lambda text: text.split()
tokenizer_porter = lambda text: [porter.stem(word) for word in text.split()]
tokenizer_snowball = lambda text: [snowball.stem(word) for word in text.split()]
tokenizer_whitelist = lambda text: [word for word in text.split() if word in semantic_words]
tokenizer_porter_wl = lambda text: [porter.stem(word) for word in text.split() if word in semantic_words]
tokenizer_snowball_wl = lambda text: [snowball.stem(word) for word in text.split() if word in semantic_words]

### Vectorizer

vect = TfidfVectorizer(binary=False,
                       stop_words=stop_words,
                       ngram_range=(1,1),
                       preprocessor=lambda text: re.sub('[^a-zA-Z]', ' ', text.lower()),
                       tokenizer=lambda text: [porter.stem(word) for word in text.split()])



#################
### Gridsearch ##
#################



X_train_feat = vect.fit_transform(X_train, y_train)
X_train_feat = X_train_feat.toarray()


clf_2 = RandomForestClassifier(n_estimators=50)


tuned_parameters = [
  {'criterion': ['gini', 'entropy'], 
   'max_features': ['auto', 'log2', 'sqrt'],
    },
 ]


grid_search_1 = GridSearchCV(clf_2, 
                           tuned_parameters, 
                           n_jobs=1, 
                           scoring='roc_auc',
                           cv=2
                )

grid_search_1.fit(X_train_feat, X_train_feat)

with open('./run_gridsearch_1.log') as log:

    log.write("Best parameters set found on development set:\n\n")
    log.write(grid_search_1.best_estimator_)
    log.write("\nGrid scores on development set:")

    for params, mean_score, scores in grid_search_1.grid_scores_:
        log.write("\n%0.3f (+/-%0.03f) for %r"
                % (mean_score, scores.std() / 2, params))