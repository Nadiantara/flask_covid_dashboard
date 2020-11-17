from altair import Chart, X, Y, Axis, Data, DataFormat
import pandas as pd
import numpy as np
from flask import render_template, url_for, flash, redirect, request, make_response, jsonify, abort
import pickle
from web import app
from web.utils import utils, altair_plot, plotly_plot
from scipy.stats import zscore
import scipy.stats as stats
import csv
import requests
import json

# Loading raw data and clean it



#loading data
total_confirmed, total_death, total_recovered, df_pop = utils.load_data()

(grouped_total_confirmed, grouped_total_recovered,
 grouped_total_death, timeseries_final, country_names) = utils.preprocessed_data(total_confirmed, total_death, total_recovered)

final_df = utils.merge_data(grouped_total_confirmed,
                            grouped_total_recovered, grouped_total_death, df_pop)

#for chart_js map
utils.load_chartjs_map_data(final_df, df_pop)


@app.route("/")
@app.route("/plotly")
def plot_plotly_global():
    # total confirmed cases globally
    total_all_confirmed = total_confirmed[total_confirmed.columns[-1]].sum()
    total_all_recovered = total_recovered[total_recovered.columns[-1]].sum()
    total_all_deaths = total_death[total_death.columns[-1]].sum()
    #ploting
    plot_global_cases_per_country = plotly_plot.plotly_global_cases_per_country(
        final_df)
    plot_global_time_series = plotly_plot.plotly_global_timeseries(
        timeseries_final)
    plot_geo_analysis = plotly_plot.plotly_geo_analysis(final_df)
    context = {"total_all_confirmed": total_all_confirmed,
               "total_all_recovered": total_all_recovered, "total_all_deaths": total_all_deaths,
            'plot_global_cases_per_country': plot_global_cases_per_country,
            'plot_global_time_series': plot_global_time_series,'plot_geo_analysis': plot_geo_analysis}
    return render_template('plotly.html', context=context)



@app.route("/altair")
def plot_altair_global():
    # total confirmed cases globally
    total_all_confirmed = total_confirmed[total_confirmed.columns[-1]].sum()
    total_all_recovered = total_recovered[total_recovered.columns[-1]].sum()
    total_all_deaths = total_death[total_death.columns[-1]].sum()
    #ploting
    plot_global_cases_per_country = altair_plot.altair_global_cases_per_country(final_df)
    plot_global_time_series = altair_plot.altair_global_time_series(
        timeseries_final)
    plot_geo_analysis = altair_plot.altair_geo_analysis(final_df)
    context = {"total_all_confirmed": total_all_confirmed,
               "total_all_recovered": total_all_recovered, "total_all_deaths": total_all_deaths,
               'plot_global_cases_per_country': plot_global_cases_per_country,
               'plot_global_time_series': plot_global_time_series, 'plot_geo_analysis': plot_geo_analysis}
    return render_template('altair.html', context=context)

    
@app.route("/chartjs")
def plot_chartjs():
    # total confirmed cases globally
    total_all_confirmed = total_confirmed[total_confirmed.columns[-1]].sum()
    total_all_recovered = total_recovered[total_recovered.columns[-1]].sum()
    total_all_deaths = total_death[total_death.columns[-1]].sum()
    countries = final_df['Country/Region'].values.tolist()
    total_values = final_df['confirmed'].values.tolist()
    cases_per_million = final_df['cases/million'].values.round(2).tolist()
    #load json file for highchart map
    with open('web/dataset/chart_js.json') as f:
        datamap = json.load(f)

    context = {"total_all_confirmed": total_all_confirmed,
               "total_all_recovered": total_all_recovered, "total_all_deaths": total_all_deaths, 
               'countries': countries, 'total_values': total_values,
               'cases_per_million': cases_per_million, 'datamap': datamap}
    return render_template('chartjs.html', context=context)
