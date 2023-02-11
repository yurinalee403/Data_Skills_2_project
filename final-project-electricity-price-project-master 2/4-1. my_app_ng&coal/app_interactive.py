#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 15:52:02 2022

@author: yoon
"""

import pandas as pd
import matplotlib.pyplot as plt
import os


#Interactive Plotting - scatterplots 
from shiny import App, render, ui, reactive
import seaborn as sns


df = pd.read_csv('raw_material.csv').drop(['units'], axis=1)
state_name = df['stateid'].unique()

app_ui = ui.page_fluid(
    ui.row(
        ui.column(4, ui.em(ui.h3('')),
                        offset=0,
                         align='center'),
        ui.column(4, ui.h1('Coal and Natural Gas'),
                     ui.hr()),
        ui.column(4, ui.input_select(id='st',
                                     label='Choose a State',
                                     choices= list(state_name)))
        ),

    ui.row(
        ui.column(6, ui.output_plot('coal')),
        ui.column(6, ui.output_table('raw_data'), align='center')
        ),
    
    ui.row(
        ui.column(7, ui.output_plot('ng')))
    )


def server(input, output, session):
    @reactive.Calc
    def get_data():
        df = pd.read_csv('raw_material.csv').drop(['units'], axis=1)
        return df[df['stateid'] == input.st()]

    
    @output
    @render.plot
    def ng():
        df = get_data()
        ax = sns.scatterplot(data=df, x='period', y='ng_price', hue='ng_price')
        ax.tick_params(axis='x', rotation=45)
        ax.set_xlabel('Year')
        ax.set_ylabel('Price($/MCF')
        ax.set_title(f'Natural Gas Price in {input.st()} over the Year')
        plt.legend(title='price range', loc='center left', bbox_to_anchor=(1, 0.5))
        return ax
    
    @output
    @render.plot
    def coal():
        df = get_data()
        ax = sns.scatterplot(data=df, x='period', y='c_price', hue='c_price')
        ax.tick_params(axis='x')
        ax.set_xlabel('Year')
        ax.set_ylabel('Price($/short ton)')
        ax.set_title(f'Coal Price in {input.st()} over the Year')
        plt.legend(title='price range', loc='center left', bbox_to_anchor=(1, 0.5))
        return ax
    
    
    @output
    @render.table
    def raw_data():
        df = get_data()
        return df

app = App(app_ui, server)
