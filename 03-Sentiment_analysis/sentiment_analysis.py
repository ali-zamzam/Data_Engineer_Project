"""importer les données dans un DataFrame nommé dataset.
Afficher les 10 premières lignes du dataset."""


import re

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import (
    CountVectorizer,
    TfidfTransformer,
    TfidfVectorizer,
)
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB  # l'algorithme Naive Byes
from sklearn.pipeline import Pipeline
from wordcloud import WordCloud

for dependency in (
    "stopwords",
    "wordnet",
    "omw-1.4",
):
    nltk.download(dependency)

# df = pd.read_csv("data/02-cashnet.csv")

# df["sentiment"] = df.loc[:, "stars"]


# df["sentiment"].replace(1, 0, inplace=True)
# df["sentiment"].replace(2, 0, inplace=True)

# df["sentiment"].replace(3, 1, inplace=True)
# df["sentiment"].replace(4, 1, inplace=True)
# df["sentiment"].replace(5, 1, inplace=True)

# df.dropna(axis=0, how="any", inplace=True)
# df.head()

# df.to_csv("data/new-cashnet.csv", index=False)


# importer les données
dataset = pd.read_csv("data/new-cashnet.csv")

# Afficher les 10 premières lignes
dataset.head()

# trouver le shape de dataset
dataset.shape
# verifier s'il ya des valeurs null
dataset.isnull().sum()

# ------------------------------------------------------------------------------------------------------------------------------
# drop les columns Title,stars
dataset = dataset[["reviews", "sentiment"]]

# Évaluer la distribution de classe stars
data = dataset["sentiment"].value_counts()

# créer une visualisation
sns.barplot(x=data.index, y=data.values)

# ------------------------------------------------------------------------------------------------------------------------------
# Compilez tous les commentaires du column reviewsdans une variable texte
txt = ""
for i in dataset.reviews:
    txt += i
print(txt)


# Initialiser une variable stop_words contenant des mots vides en anglais.

stop_words = set(stopwords.words("english"))
print(stop_words)

# ------------------------------------------------------------------------------------------------------------------------------
# générer un word cloud
from wordcloud import WordCloud

wc = WordCloud(
    background_color="black",
    max_words=300,
    stopwords=stop_words,
    max_font_size=50,
    random_state=42,
)

"""afficher le wordcloud"""

import matplotlib.pyplot as plt

plt.figure(figsize=(15, 15))  # Figure initialization
wc.generate(txt)  # "Calculation" from the wordcloud
plt.imshow(wc)  # Display
plt.show()
# ------------------------------------------------------------------------------------------------------------------------------
def text_cleaning(text, remove_stop_words=True, lemmatize_words=True):
    # Nettoyer le texte, avec la possibilité de supprimer les stop_words et de lemmatiser le mot
    # Nettoyer le texte
    text = re.sub(r"[^A-Za-z0-9]", " ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"http\S+", " link ", text)
    text = re.sub(r"\b\d+(?:\.\d+)?\s+", "", text)  # remove numbers

    # Supprimer la ponctuation du texte
    # text = "".join([c for c in text if c not in punctuation])

    # Optionnelle, supprimez les mots vides
    if remove_stop_words:
        text = text.split()
        text = [w for w in text if not w in stop_words]
        text = " ".join(text)

    # Optionnelle, raccourcir les mots à leurs racine
    if lemmatize_words:
        text = text.split()
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in text]
        text = " ".join(lemmatized_words)

    # Return a list of words
    return text


# nltk.download('wordnet')
# nltk.download('omw-1.4')
# appliquer la fonction text cleaning
dataset["cleaned_review"] = dataset["reviews"].apply(text_cleaning)

# ------------------------------------------------------------------------------------------------------------------------------
#  créer les variables (features et target)
train_data = dataset["cleaned_review"]

y_target = dataset["sentiment"]


# Diviser les matrices en un ensemble d'entraînement et un ensemble de test

X_train, X_test, y_train, y_test = train_test_split(
    train_data, y_target, test_size=0.25, random_state=42, shuffle=True
)


pipeline = Pipeline(
    [
        ("tfidf", TfidfTransformer()),
        ("classifier", MultinomialNB()),
    ]
)

modele = pipeline.fit(X_train, y_train)

y_pred = modele.predict(X_test)

# ------------------------------------------------------------------------------------------------------------------------------
# Afficher le rapport de la classification
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))


print("Accuracy Train: {}".format(accuracy_score(y_test, y_pred)))

# afficher la confusion matrix

import scikitplot as skplt

skplt.metrics.plot_confusion_matrix(y_test, y_pred, normalize=True)
plt.show()


confusion_matrix = pd.crosstab(
    y_test, y_pred, rownames=["Real Class"], colnames=["Predicted Class"]
)
print(confusion_matrix)

# ------------------------------------------------------------------------------------------------------------------------------
# sauvgarder le model de la prediction
import joblib

joblib.dump(modele, "data/model.pkl")
