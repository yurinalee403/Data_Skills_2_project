

#2. Plotting
##1) Static Plots
import pandas as pd
import matplotlib.pyplot as plt
import os


#Coal
coal = pd.read_csv('df2.csv')

def plot_by_group(coal, x_axis, y_axis, value):
    # showing the average price 
    c = coal.groupby(x_axis)[y_axis].mean()

    c.plot(label='Average Price Change in Electricity', color='orange', 
            marker='o', markerfacecolor='purple', legend=True)
    plt.xlabel('Year')
    plt.ylabel('Price ($/dollars per short ton)')
    plt.tight_layout


plot_by_group(coal, 'period', 'price', 'avg')
plt.savefig('static_coal.png',  facecolor='w', bbox_inches="tight", pad_inches=0.3, transparent=True)





#Natural Gas
ngas = pd.read_csv('natural_gas.csv')

ngas_plot = ngas.loc[ngas.stateid == 'U.S.'].sort_values(by='period', ascending=True).reset_index(drop=True)
ngas_plot

#Get average value in 2011
ngas_2011 = ngas[ngas['period'] == 2011]
avg = round(sum(ngas_2011['value'])/len(ngas_2011['value']),2)

ngas_plot.loc[0] = ['2011', 'U.S.', avg, '$/MCF']
ngas_plot.head()


ngas_plot = ngas_plot.drop(['stateid', 'units'], axis=1).set_index('period')
ngas_plt = ngas_plot.rename(columns = {'value' :'price'})
ngas_plt.head()


ax = ngas_plt.plot(kind = 'line', title=['Average Price Change in Natural Gas'], subplots = True, rot = 0, 
                              linewidth=2, color='pink', xlabel = 'Year', ylabel = 'Price($/MCF)',
                              fontsize = 12, marker='o', markerfacecolor='purple', logy=False,
                              figsize = (100, 50), layout=(10, 12), legend = True)

plt.tight_layout
plt.savefig('static_ng.png',  facecolor='w', bbox_inches="tight", pad_inches=0.3, transparent=True) 




#Electricity Price
eprice = pd.read_csv('E_Price.csv')

eprice_ave = eprice.groupby(['period'])['price'].mean().reset_index()
eprice_ave

eprice_ave['period'] = eprice_ave['period'].astype(str)
eprice_ave = eprice_ave.set_index('period')


ax = eprice_ave.plot(kind = 'line', title=['Average Price Change in Electricity'], subplots = True, rot = 0, 
                              linewidth=2, color='skyblue', xlabel = 'Year', ylabel = 'Price(cents per kilowatthour)',
                              fontsize = 12, marker='o', markerfacecolor='purple', logy=False,
                              figsize = (100, 50), layout=(10, 12))

plt.tight_layout
plt.savefig('static_E.png',  facecolor='w', bbox_inches="tight", pad_inches=0.3, transparent=True)  
