from altair import Chart, X, Y, Axis, Data, DataFormat
import pandas as pd
import numpy as np
from flask import render_template, url_for, flash, redirect, request, make_response, jsonify, abort
from web import app
from web.utils import utils, altair_plot, plotly_plot
import json

# Loading raw data and clean it



#loading data
total_confirmed, total_death, total_recovered, df_pop = utils.load_data()

(grouped_total_confirmed, grouped_total_recovered,
 grouped_total_death, timeseries_final, country_names) = utils.preprocessed_data(total_confirmed, total_death, total_recovered)

final_df = utils.merge_data(grouped_total_confirmed,
                            grouped_total_recovered, grouped_total_death, df_pop)

#for chart_js map



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
    
    #  time series for each cases
    confirmed_timeseries = timeseries_final["daily new cases"].values.tolist()
    death_timeseries = timeseries_final["daily new deaths"].values.tolist()
    recovered_timeseries = timeseries_final["daily new recovered"].values.tolist()
    timeseries_dates = timeseries_final["date"].values.tolist()
    #load json file for highchart map
    datamap = utils.load_chartjs_map_data(final_df, df_pop)

    context = {"total_all_confirmed": total_all_confirmed,
               "total_all_recovered": total_all_recovered, "total_all_deaths": total_all_deaths,
               "confirmed_timeseries": confirmed_timeseries, "death_timeseries": death_timeseries,
               "recovered_timeseries": recovered_timeseries, 'timeseries_dates': timeseries_dates,
               'countries': countries, 'total_values': total_values,
               'cases_per_million': cases_per_million, 'datamap': datamap}
    return render_template('chartjs.html', context=context)


@app.route("/country", methods=['POST'])
def plot_country():
    # total confirmed cases globally
    # take country input from user
    country_name = request.form['country_name']
    total_confirmed_per_country, total_death_per_country, total_recovered_per_country=utils.get_per_country_data(
            total_confirmed, total_death, total_recovered, country_name)
    #ploting
    #plotly
    plotly_country_plot = plotly_plot.plotly_per_country_time_series(total_confirmed, 
                                                            total_death, total_recovered, country_name)
    #altair
    altair_country_plot = altair_plot.altair_per_country_time_series(total_confirmed, 
                                                            total_death, total_recovered, country_name)
    #chart.js variable
    timeseries_country = utils.get_by_country_merged(
        total_confirmed, total_death, total_recovered, country_name)
    
    confirmed_timeseries = timeseries_country["daily_new_confirmed"].values.tolist()
    death_timeseries = timeseries_country["daily_new_death"].values.tolist()
    recovered_timeseries = timeseries_country["daily_new_recovered"].values.tolist()
    timeseries_dates = timeseries_country["date"].values.tolist()
    context = {"total_confirmed_per_country": total_confirmed_per_country,
            "total_death_per_country": total_death_per_country, "total_recovered_per_country": total_recovered_per_country,
            'plotly_country_plot': plotly_country_plot, 'altair_country_plot': altair_country_plot,
               "confirmed_timeseries": confirmed_timeseries, "death_timeseries": death_timeseries,
               "recovered_timeseries": recovered_timeseries, "timeseries_dates": timeseries_dates}
    return render_template('country.html', context=context)
