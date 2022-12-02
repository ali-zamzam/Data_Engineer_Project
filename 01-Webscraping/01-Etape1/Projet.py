# ok:   le nombre d’avis, la note Trustscore,

# en cours : domaine,les pourcentages sur chaque classe de commentaires(le pourcentage d’avis Excellent))
# L’autre regroupant l’ensemble des commentaires d’une entreprise avec plus de 10000 avis (ShowRoom par exemple),
#  avec les informations liées à l’avis(nombre d’étoile, si l’entreprise a répondu à l’avis négatif)
# ------------------------------------------------------------------------------------------------
# Etape1
# ------------------------------------------------------------------------------------------------
import csv
import json
from random import randint
from time import sleep
from urllib.request import urlopen

import pandas as pd
import requests
from bs4 import BeautifulSoup

page_SC = urlopen(
    "https://www.trustpilot.com/categories/financial_institution?sort=reviews_count"
)

soup = BeautifulSoup(page_SC, "html.parser")

noms_SC = soup.findAll(
    name="p",
    attrs={
        "class": "typography_heading-xs__D8ZZo typography_appearance-default__3vWd5 styles_displayName__1LIcI"
    },
)
entreprise = []

for element in noms_SC:
    entreprise.append(element.text)

print(entreprise)
# ----------------------------------------------------------------------------------------------------------------

liste1 = []
domaine = []
for score in soup.findAll(
    name="span",
    attrs={"class": "typography_body-s__1oUdA typography_appearance-default__3vWd5"},
):
    liste1.append(score.text)

print(liste1)

for i in liste1:
    i = "Financial Institution"
    domaine.append(i)

print(domaine)
# ----------------------------------------------------------------------------------------------------------
trust_score = []

for score in soup.findAll(
    name="span",
    attrs={
        "class": "typography_body-m__3GWSM typography_appearance-subtle__2GxHy styles_trustScore__nLHX2"
    },
):
    #  weuse strip to eleminate the ( ) becase on the site we have the date like that (1957)
    trust_score.append(score.text.strip("TrustScore "))

print(trust_score)

# ------------------------------------------------------------------------------------------------
liste = []

for score in soup.findAll(
    name="p",
    attrs={
        "class": "typography_body-m__3GWSM typography_appearance-subtle__2GxHy styles_ratingText__nheL7"
    },
):
    liste.append(score.text)
# print(liste)


result1 = []
for i in liste:
    result1.append(i.split("|")[1])

# print(result1)


f_result = []
for i in result1:

    f_result.append(i.strip(" reviews"))

n_avis = f_result

print(n_avis)
# ------------------------------------------------------------------------------------------------

liste = [
    "advanceamerica.net",
    "onemainfinancial.com",
    "moneylion.com",
    "www.mtrustcompany.com",
    "www.cashnetusa.com",
    "www.spotloan.com",
    "www.lendio.com",
    "smartbizloans.com",
    "mymoneytogo.com",
    "biz2credit.com",
    "towerloan.com",
    "1ffc.com",
    "www.netspend.com",
    "amscot.com",
    "netcredit.com",
    "americor.com",
    "newdayusa.com",
    "www.dontbebroke.com",
    "mytresl.com",
    "www.freedomplus.com",
]

avis_excellentes = []

for i in liste:
    url = f"https://www.trustpilot.com/review/{i}"
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")

    for review in soup.find_all(
        "div",
        attrs={
            "class": "paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv styles_reviewsOverview__mVIJQ"
        },
    ):
        # Review titles
        review_title = review.find(
            "p",
            attrs={
                "class": "typography_body-m__xgxZ_ typography_appearance-default__AAY17 styles_cell__qnPHy styles_percentageCell__cHAnb"
            },
        )
        avis_excellentes.append(review_title.text)

print(avis_excellentes)

# ------------------------------------------------------------------------------------------------
Etape1 = pd.DataFrame(
    list(zip(entreprise, trust_score, n_avis, avis_excellentes, domaine)),
    columns=["Entreprise", "Trust_score", "N_avis", "Avis_excellentes", "Domaine"],
)

Etape1.head()
Etape1.to_csv("generated_data/Etape1.csv", index=False)

# to save the dataframe
# Etape1.to_csv("generated_data/Ex1.csv", index=False)
