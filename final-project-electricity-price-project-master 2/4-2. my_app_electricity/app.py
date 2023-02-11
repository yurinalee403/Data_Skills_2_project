from shiny import App, render, ui, reactive
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


path = "C:/Users/wynbu/Desktop/Python Final/my_app/"
eprice = pd.read_csv(path + 'E_Price.csv')

eprice = eprice.dropna()
eprice

eprice = eprice[eprice['sectorName'].apply(lambda i: i in ['residential'])]
eprice = eprice.drop(columns = ['Unnamed: 0','stateDescription','sectorid','price-units','sectorName'])

eprice['period'] = eprice['period'].astype(str)
eprice = eprice.set_index('period')

state_name = eprice['stateid'].unique()

app_ui = ui.page_fluid(
    ui.row(
        ui.column(4, ui.em(ui.h3('')),
                        offset=0,
                         align='center'),
        ui.column(4, ui.h1('Electricy'),
                     ui.hr()),
        ui.column(4, ui.input_select(id='st',
                                     label='Choose a State',
                                     choices= list(state_name)))
        ),

    ui.row(
        ui.column(6, ui.output_plot('Electricy')),
        ui.column(6, ui.output_table('raw_data'), align='center')
        )
    )


def server(input, output, session):
    @reactive.Calc
    def get_data():
        path = "C:/Users/wynbu/Desktop/Python Final/my_app/"
        eprice = pd.read_csv(path + 'E_Price.csv')

        eprice = eprice.dropna()
        eprice

        eprice = eprice[eprice['sectorName'].apply(lambda i: i in ['residential'])]
        eprice = eprice.drop(columns = ['Unnamed: 0','stateDescription','sectorid','price-units','sectorName'])

        eprice['period'] = eprice['period'].astype(str)
        eprice = eprice.set_index('period')

        state_name = eprice['stateid'].unique()
        return eprice[eprice['stateid'] == input.st()]

    
    @output
    @render.plot
    def Electricy():
        df = get_data()
        ax = sns.scatterplot(data=df, x='period', y='price', hue='price')
        ax.tick_params(axis='x', rotation=45)
        ax.set_xlabel('Year')
        ax.set_ylabel('Price(cents per kilowatthour)')
        ax.set_title(f'Electricity Price in {input.st()} over the Year')
        plt.legend(title='price range', loc='center left', bbox_to_anchor=(1, 0.5))
        return ax

    @output
    @render.table
    def raw_data():
        df = get_data()
        return df


app = App(app_ui, server)
