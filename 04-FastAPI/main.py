import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

import joblib
import nltk
import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from nltk.corpus import stopwords
from passlib.context import CryptContext
from pydantic import BaseModel

nltk.download("stopwords")
app = FastAPI(
    title="Analyse des Sentiments",
    description="Une API pour analyser les sentiments des avis Trustpilot",
    version="1.0",
)


# class Prediction(BaseModel):
#     review: str


class Users(BaseModel):
    username: str
    password: str


security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


with open("model.pkl", "rb") as f:
    model = joblib.load(f)


# class Prediction(BaseModel):
#     review: str

admin = {
    "admin": {
        "username": "admin",
        "password": pwd_context.hash("ADMIN12345"),
    }
}

users_db = {
    "ali": {
        "username": "ali",
        "password": pwd_context.hash("AZ12345"),
    },
    "dan": {
        "username": "dan",
        "password": pwd_context.hash("DA12345"),
    },
    "andre": {
        "username": "andre",
        "password": pwd_context.hash("AN12345"),
    },
}


def get_current_admin(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not (admin.get(username)) or not (
        pwd_context.verify(credentials.password, admin[username]["password"])
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not (users_db.get(username)) or not (
        pwd_context.verify(credentials.password, users_db[username]["password"])
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/user")
def current_user(username: str = Depends(get_current_user)):
    return "Hello {}".format(username)


# cleaning the data
def text_cleaning(text, remove_stop_words=True):
    # Clean the text, with the option to remove stop_words and to lemmatize word
    # Clean the text
    text = re.sub(r"[^A-Za-z0-9]", " ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"http\S+", " link ", text)
    text = re.sub(r"\b\d+(?:\.\d+)?\s+", "", text)  # remove numbers

    # Optionally, remove stop words
    if remove_stop_words:
        # load stopwords
        stop_words = stopwords.words("english")
        text = text.split()
        text = [w for w in text if not w in stop_words]
        text = " ".join(text)

    return text


@app.post("/sentiments-prediction")
async def predict_sentiment(review: str, cleaned_review=Depends(get_current_user)):
    # clean the review
    cleaned_review = text_cleaning(review)

    #  prediction
    analyse = int(model.predict([[cleaned_review]][0]))
    score = model.predict_proba([[cleaned_review]][0])
    output_score = str(round(float(score[:, analyse]), 2))

    # output
    if analyse == 0:
        analyse = "Negative"
    else:
        analyse = "Positive"

    return {"prediction": analyse, "score": output_score}


@app.put("/users")
def put_users(user: Users, use=Depends(get_current_admin)):
    username = user.username
    users_db[username] = user.dict()
    password = user.password
    users_db[password] = user.dict()
    return {f"{username}successfully added"}


@app.delete("/users/{username}")
def delete_users(username: str, use=Depends(get_current_admin)):
    del users_db[username]
    return {f"{username} successfully deleted"}
