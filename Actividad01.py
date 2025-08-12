import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

dat=pd.read_csv('Censo2017_Manzanas.csv',delimiter=';')

#Visualizar las primeras lineas
dat.head()
dat.info()
#Total de población
total_pop=dat['PERSONAS'].sum()
print(f'Población total en 2017: {total_pop}')
#Distribución por edad y género
cols=['EDAD_0A5','EDAD_6A14','EDAD_15A64','EDAD_65YMAS']
for col in cols:
    dat[col]=dat[col].replace('*',0).astype(float)
    
pv=pd.pivot_table(dat, index='REGION', values=cols, aggfunc='sum', margins=False)
pv

fig = plt.figure(figsize=(11,3))
ax = fig.add_subplot(111)
ax.set_ylabel('Número de personas')
fig.suptitle('Distribución de población por Edad y Región (Chile, Censo 2017)')
pv.plot(kind='bar', ax =ax);

#Leer datos censales
manz=gpd.read_file('R13/MANZANA_IND_C17.shp')
com=gpd.read_file('R13/COMUNA_C17.shp')

com.plot()
manz.head()

from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as colors

#Crear figura y ejes
fig=plt.figure(figsize=(13,13))
ax=fig.add_subplot(111)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

# cantidad de personas por manzana
Z=manz['TOTAL_PERS']
manz.plot(ax=ax, column='TOTAL_PERS', cmap='Reds', legend=True, vmin=0, vmax=1000)

com_projected = com.to_crs(epsg=3857)
com_projected.boundary.plot(ax=ax, lw=0.2, color='k')

xlim=[-70.9,-70.4]
ylim=[-33.7,-33.2]
for x, y, label in zip(com_projected.geometry.centroid.x, com_projected.geometry.centroid.y, com_projected.NOM_COMUNA):
    if xlim[0]<x<xlim[1] and ylim[0]<y<ylim[1]:
        ax.text(x, y, label, fontsize = 10)
        
ax.set_xlim(xlim)
ax.set_ylim(ylim);

## Reemplace 'XXX' por su apellido
ax.set_title('RM - Población total por manzana - Censo 2017 - Ejecutado por loayza',fontsize=10)

## Reemplace 'XXX' por su apellido en el nombre del archivo de salida 
fig.savefig('PoblacionRM_C2017_UC.jpg')