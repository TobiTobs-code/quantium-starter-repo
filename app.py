import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

DATA_FILE = "formatted_output.csv"

df = pd.read_csv(DATA_FILE)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

app = dash.Dash(__name__)

region_options = [
    {"label": "All", "value": "all"},
    {"label": "North", "value": "north"},
    {"label": "East", "value": "east"},
    {"label": "South", "value": "south"},
    {"label": "West", "value": "west"}
]

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "background": "linear-gradient(135deg, #fff1f2 0%, #f8fafc 45%, #eef2ff 100%)",
        "fontFamily": "Arial, sans-serif",
        "padding": "32px",
        "color": "#1f2937"
    },
    children=[
        html.Div(
            style={
                "maxWidth": "1100px",
                "margin": "0 auto"
            },
            children=[
                html.Div(
                    style={
                        "textAlign": "center",
                        "marginBottom": "32px"
                    },
                    children=[
                        html.H1(
                            "Soul Foods Pink Morsels Sales Visualiser",
                            style={
                                "fontSize": "38px",
                                "marginBottom": "10px",
                                "color": "#be123c"
                            }
                        ),
                        html.P(
                            "Explore Pink Morsels sales by region before and after the price increase on 15 January 2021.",
                            style={
                                "fontSize": "17px",
                                "color": "#4b5563",
                                "margin": "0 auto",
                                "maxWidth": "760px"
                            }
                        )
                    ]
                ),

                html.Div(
                    style={
                        "background": "white",
                        "borderRadius": "18px",
                        "padding": "24px",
                        "boxShadow": "0 12px 30px rgba(15, 23, 42, 0.12)",
                        "marginBottom": "24px"
                    },
                    children=[
                        html.H2(
                            "Filter by Region",
                            style={
                                "fontSize": "20px",
                                "marginBottom": "12px",
                                "color": "#111827"
                            }
                        ),
                        dcc.RadioItems(
                            id="region-filter",
                            options=region_options,
                            value="all",
                            inline=True,
                            style={
                                "display": "flex",
                                "gap": "18px",
                                "flexWrap": "wrap",
                                "fontSize": "15px"
                            },
                            labelStyle={
                                "background": "#fce7f3",
                                "padding": "10px 14px",
                                "borderRadius": "999px",
                                "cursor": "pointer",
                                "fontWeight": "600",
                                "color": "#831843"
                            }
                        )
                    ]
                ),

                html.Div(
                    style={
                        "background": "white",
                        "borderRadius": "18px",
                        "padding": "24px",
                        "boxShadow": "0 12px 30px rgba(15, 23, 42, 0.12)"
                    },
                    children=[
                        dcc.Graph(id="sales-line-chart")
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df.copy()
        title_region = "All Regions"
    else:
        filtered_df = df[df["Region"].str.lower() == selected_region].copy()
        title_region = selected_region.title()

    daily_sales = filtered_df.groupby("Date", as_index=False)["Sales"].sum()

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title=f"Pink Morsels Sales Over Time - {title_region}",
        labels={
            "Date": "Date",
            "Sales": "Total Sales"
        }
    )

    fig.update_traces(
        line=dict(width=3),
        mode="lines"
    )

    fig.update_layout(
        plot_bgcolor="#f8fafc",
        paper_bgcolor="white",
        title={
            "font": {"size": 22},
            "x": 0.02
        },
        xaxis_title="Date",
        yaxis_title="Total Sales",
        font={
            "family": "Arial, sans-serif",
            "size": 14,
            "color": "#1f2937"
        },
        margin={
            "l": 60,
            "r": 30,
            "t": 70,
            "b": 60
        }
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)