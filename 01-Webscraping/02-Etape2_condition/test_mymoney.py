from random import randint
from time import sleep
from urllib.request import urlopen

import pandas as pd
import requests
from bs4 import BeautifulSoup

page = 1
n_stars = []
reviews = []
rate = []
reponse = []
int_rate = []
title = []
while page != 600:
    url = f"https://www.trustpilot.com/review/mymoneytogo.com?page={page}"
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    for titles in soup.find_all(
        name="a",
        attrs={
            "class": "link_internal__7XN06 typography_appearance-default__AAY17 typography_color-inherit__TlgPO link_link__IZzHN link_notUnderlined__szqki"
        },
    ):

        title.append(titles.text.strip(" "))

    for review in soup.find_all(
        name="p",
        attrs={
            "class": "typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"
        },
    ):
        if review == " ":
            reviews.append("NaN")
        else:
            reviews.append(review.text.strip(" "))

    for reply in soup.find_all(
        "p",
        attrs={
            "class": "typography_body-m__xgxZ_ typography_appearance-default__AAY17 styles_message__shHhX"
        },
    ):
        reponse.append(reply.text.strip(" "))

    for star in soup.find_all(
        "div",
        attrs={
            "class": "styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ"
        },
    ):
        # Review titles
        review_title = star.find(
            "div",
            attrs={"class": "star-rating_starRating__4rrcf star-rating_medium__iN6Ty"},
        ).findChild()
        if title == " " or reviews == " ":
            n_stars.append("NaN")
        else:
            n_stars.append(review_title["alt"].strip("Rated"))

    rate1 = []
    for i in n_stars:
        rate1.append(i.split("out")[0])

    # print(rate1)

    rate2 = []
    for i in rate1:

        rate2.append(i.strip("Rated "))
        rate = rate2

        # int_rate = list(map(int, rate))
    # print(int_rate)
    page = page + 1
    sleep(randint(2, 10))


mymoney = pd.DataFrame(
    list(zip(title, reviews, rate)),
    columns=["Title", "reviews", "stars"],
)


# to save the dataframe
mymoney.to_csv("../csv_final/mymoney.csv", index=False)
