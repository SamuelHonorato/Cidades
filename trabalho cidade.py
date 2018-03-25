from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
 
map = Basemap(projection='merc',
              lat_0 = 0, lon_0 = 0,
              resolution = 'h',
              area_thresh = 0.1,
              llcrnrlon=-42,
              llcrnrlat=-7.9,
              urcrnrlon=-37,
              urcrnrlat=-2.7)

map.drawcoastlines()
map.drawcountries()
map.drawstates()
map.fillcontinents(color='#cc9955', lake_color='aqua')
map.drawmapboundary(fill_color='aqua')
 
lons = [-39.047547,-38.705624,-40.118241,-39.455705]
lats = [-7.356977,-4.223138,-2.885311,-6.092762]
 
x,y = map(lons, lats)
map.plot(x, y, 'bo', markersize=5)
 
labels = ['ABAIARA','ACARAPE','ACARAU','ACOPIARA']
 
for label, xpt, ypt in zip(labels, x, y):
    plt.text(xpt+10000, ypt+5000, label)
 
plt.show()

