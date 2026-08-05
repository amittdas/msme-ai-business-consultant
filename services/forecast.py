import pandas as pd
import os

from sklearn.linear_model import LinearRegression

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "business_data.csv")


def predict_next_month():

    df = pd.read_csv(CSV_PATH)

    X = [[i] for i in range(len(df))]
    y = df["Sales"]

    model = LinearRegression()

    model.fit(X, y)

    next_month = [[len(df)]]

    prediction = model.predict(next_month)

    return int(prediction[0])
