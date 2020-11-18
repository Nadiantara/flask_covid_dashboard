import pandas as pd
import numpy as np
import dateutil
import datetime
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import altair as alt
from vega_datasets import data
from plotly.subplots import make_subplots
import plotly.express as px
import json
from web.utils.utils import get_by_country_merged

def plotly_geo_analysis(final_df):
    #Plotly plot 1: Geographical analysis
    df = final_df

    fig = go.Figure(data=go.Choropleth(
        locations=df['code3'],
        z=df['confirmed'],
        text=df['Country/Region'],
        colorscale='Darkmint',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix='',
        colorbar_title='#confirmed',
    ))

    fig.update_layout(
        title={'text': "Total Confirmed Cases by Country",
               'y': 0.9,
               'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations=[dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://github.com/CSSEGISandData/COVID-19">\
                CSSE at Johns Hopkins University</a>',
            showarrow=False
        )],
        width=700, height=600
    )
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json


def plotly_global_cases_per_country(final_df):
    # Plotly plot 2: Per country total cases and cases/million populations

    df = final_df
    #print(df.head())
    df.index = df['Country/Region']
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["confirmed"],
            name="# of confirmed cases",
            marker_color='#39ac39',
            opacity=1
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["cases/million"],
            mode="lines",
            name="cases/million",
            marker_color='#b23434',
            opacity=0.7
        ),
        secondary_y=True
    )

    # Add figure title
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=0.93),
        title={
        'text': '<span style="font-size: 20px;">Global aggregate cases</span><br><span style="font-size: 10px;">(click and drag)</span>',
        'y': 0.97,
        'x': 0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        width=1500, height=700
    )

    # Set x-axis title
    fig.update_xaxes(tickangle=45)

    # Set y-axes titles
    fig.update_yaxes(title_text="# of confirmed cases",
                     secondary_y=False, showgrid=False)
    fig.update_yaxes(title_text="cases/millions", tickangle=45,
                     secondary_y=True, showgrid=False)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json


def plotly_global_timeseries(timeseries_final):
    #Plotly plot 3: Global time series chart for daily new cases, recovered, and deaths
    df = timeseries_final
    #notice that I use plotly express (px) not graph_objects as before, just for more variances
    fig = px.line(df, x='date', y=[
                  'daily new cases', 'daily new recovered', 'daily new deaths'], title='Global daily new cases')

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(width=1500, height=500)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json


def plotly_per_country_time_series(total_confirmed, total_death, total_recovered, country_name):
    #Plotly plot 3a per country time series chart for daily new cases, recovered, and deaths
    # I use Indonesia data
    df = get_by_country_merged(
        total_confirmed, total_death, total_recovered, country_name)
    #column name: date	value_confirmed	daily_new_confirmed	value_death	daily_new_death	value_recovered	daily_new_recovered

    fig = px.line(df, x='date', y=['daily_new_confirmed', 'daily_new_death',
                                   'daily_new_recovered'], title=f'{country_name} daily  cases')

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(width=1500, height=500)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json
