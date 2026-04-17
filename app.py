import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

DATA_FILE = "formatted_output.csv"

df = pd.read_csv(DATA_FILE)

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

daily_sales = df.groupby("Date", as_index=False)["Sales"].sum()

app = dash.Dash(__name__)

fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsels Sales Over Time",
    labels={
        "Date": "Date",
        "Sales": "Total Sales"
    }
)

app.layout = html.Div(
    children=[
        html.H1(
            "Soul Foods Pink Morsels Sales Visualiser",
            style={"textAlign": "center"}
        ),
        html.P(
            "This line chart visualises Pink Morsels sales over time to compare sales before and after the price increase on 15 January 2021.",
            style={"textAlign": "center"}
        ),
        dcc.Graph(
            id="sales-line-chart",
            figure=fig
        )
    ],
    style={
        "maxWidth": "1000px",
        "margin": "0 auto",
        "padding": "24px"
    }
)

if __name__ == "__main__":
    app.run(debug=True)