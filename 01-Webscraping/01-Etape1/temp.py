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
Etape1.to_csv("generated_data/Etape1.csv")

# to save the dataframe
# Etape1.to_csv("generated_data/Ex1.csv", index=False)


# def csv_to_json(csvFilePath, jsonFilePath):
#     jsonArray = []

#     # read csv file
#     with open(csvFilePath, encoding="utf-8") as csvf:
#         # load csv file data using csv library's dictionary reader
#         csvReader = csv.DictReader(csvf)

#         # convert each csv row into python dict
#         for row in csvReader:
#             # add this python dict to json array
#             jsonArray.append(row)

#     # convert python jsonArray to JSON String and write to file
#     with open(jsonFilePath, "w", encoding="utf-8") as jsonf:
#         jsonString = json.dumps(jsonArray, ensure_ascii=False, indent=4)
#         jsonf.write(jsonString)


# csvFilePath = "generated_data/Ex1.csv"
# jsonFilePath = "generated_data/Ex1.json"
# csv_to_json(csvFilePath, jsonFilePath)
# ------------------------------------------------------------------------------------------------
# csvFilePath = "generated_data/Etape1.csv"
# jsonFilePath = "generated_data/Ex2.json"

# data = {}
# with open(csvFilePath) as csvFile:
#     csvReader = csv.DictReader(csvFile)
#     for rows in csvReader:
#         id1 = rows[""]
#         data[id1] = rows

# with open(jsonFilePath, "w") as jsonFile:
#     jsonFile.write(json.dumps(data, ensure_ascii=False, indent=4))

# ------------------------------------------------------------------------------------------------

# csvFilePath = "generated_data/Etape1.csv"
# jsonFilePath = "generated_data/Ex3.json"

# data = {}
# with open(csvFilePath) as csvFile:
#     csvReader = csv.DictReader(csvFile)
#     for rows in csvReader:
#         id1 = rows["Entreprise"]
#         data[id1] = rows

# with open(jsonFilePath, "w") as jsonFile:
#     jsonFile.write(json.dumps(data, ensure_ascii=False, indent=4))

# ------------------------------------------------------------------------------------------------
""" Etape2"""
# ------------------------------------------------------------------------------------------------
page = 1
n_stars = []
reviews_ad = []
rate = []
while page != 680:
    url = f"https://www.trustpilot.com/review/advanceamerica.net?page={page}"
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    for review in soup.find_all(
        name="p",
        attrs={
            "class": "typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"
        },
    ):
        reviews_ad.append(review.text.strip(" "))

    for review in soup.find_all(
        "div",
        attrs={
            "class": "styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ"
        },
    ):
        # Review titles
        review_title = review.find(
            "div",
            attrs={"class": "star-rating_starRating__4rrcf star-rating_medium__iN6Ty"},
        ).findChild()
        n_stars.append(review_title["alt"].strip("Rated"))

    # print(rate_review)

    rate1 = []
    for i in n_stars:
        rate1.append(i.split("out")[0])

    # print(rate1)

    rate2 = []
    for i in rate1:

        rate2.append(i.strip("Rated "))
        rate = rate2

    page = page + 1
    sleep(randint(2, 10))
    # print(rate)

Advance_America = pd.DataFrame(
    list(zip(reviews_ad, rate)), columns=["reviews_ad", "stars"]
)

Advance_America.head()

# to save the dataframe
Advance_America.to_csv("generated_data/Advance_America.csv")


# ---------------------------------------------------------------------------------------------
# page = 1
# reviews2 = []
# while page != 800:
#     url = f"https://www.trustpilot.com/review/moneylion.com?page={page}"
#     response = requests.get(url)
#     html = response.content
#     soup = BeautifulSoup(html, "html.parser")
#     for review in soup.find_all(
#         name="p",
#         attrs={
#             "class": "typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"
#         },
#     ):
#         reviews2.append(review.text.strip(" "))
#     page = page + 1
#     sleep(randint(2, 10))

# print(reviews2)


# moneylion = pd.DataFrame(list(zip(reviews2)), columns=["moneylion_reviews"])

# moneylion.head()

# # to save the dataframe
# moneylion.to_csv("generated_data/moneylion.csv")


# --------------------------------------------------------------------------------------------------------------------------------
# page = 1
# reviews3 = []
# while page != 700:
#     url = f"https://www.trustpilot.com/review/www.mtrustcompany.com?page={page}"
#     response = requests.get(url)
#     html = response.content
#     soup = BeautifulSoup(html, "html.parser")
#     for review in soup.find_all(
#         name="p",
#         attrs={
#             "class": "typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"
#         },
#     ):
#         reviews3.append(review.text.strip(" "))
#     page = page + 1
#     sleep(randint(2, 10))

# print(reviews3)


# Millennium_Trust = pd.DataFrame(
#     list(zip(reviews3)), columns=["Millennium_Trust_reviews"]
# )
# Millennium_Trust.head()

# # to save the dataframe
# Millennium_Trust.to_csv("generated_data/Millennium_Trust.csv")

# --------------------------------------------------------------------------------------------------------------------------------
# page = 1
# reviews4 = []
# while page != 700:
#     url = f"https://www.trustpilot.com/review/www.cashnetusa.com?page={page}"
#     response = requests.get(url)
#     html = response.content
#     soup = BeautifulSoup(html, "html.parser")
#     for review in soup.find_all(
#         name="p",
#         attrs={
#             "class": "typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"
#         },
#     ):
#         reviews4.append(review.text.strip(" "))
#     page = page + 1
#     sleep(randint(2, 10))

# print(reviews4)


# CashNetUSA = pd.DataFrame(list(zip(reviews4)), columns=["CashNetUSA_reviews"])
# CashNetUSA.head()

# # to save the dataframe
# CashNetUSA.to_csv("generated_data/CashNetUSA.csv")

# -------------------------------------------------------------------------------------------------------
# page = 1
# reviews5 = []
# while page != 700:
#     url = f"https://www.trustpilot.com/review/onemainfinancial.com?page={page}"
#     response = requests.get(url)
#     html = response.content
#     soup = BeautifulSoup(html, "html.parser")
#     for review in soup.find_all(
#         name="p",
#         attrs={
#             "class": "typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"
#         },
#     ):
#         reviews5.append(review.text.strip(" "))
#     page = page + 1
#     sleep(randint(2, 10))

# print(reviews5)


# onemain = pd.DataFrame(list(zip(reviews5)), columns=["onemain_reviews"])
# onemain.head()

# # to save the dataframe
# onemain.to_csv("generated_data/onemain.csv")
# ---------------------------------------------------------------------------------------------

# page = 1
# reviews6 = []
# while page != 670:
#     url = f"https://www.trustpilot.com/review/www.spotloan.com?page={page}"
#     response = requests.get(url)
#     html = response.content
#     soup = BeautifulSoup(html, "html.parser")
#     for review in soup.find_all(
#         name="p",
#         attrs={
#             "class": "typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"
#         },
#     ):
#         reviews6.append(review.text.strip(" "))
#     page = page + 1
#     sleep(randint(2, 10))

# print(reviews6)


# spotloan = pd.DataFrame(list(zip(reviews6)), columns=["spotloan_reviews"])
# spotloan.head()

# # to save the dataframe
# spotloan.to_csv("generated_data/spotloan.csv")

# -------------------------------------------------------------------------------------------
