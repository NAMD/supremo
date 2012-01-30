'''
Created on Jan 25, 2012

@author: cyg
'''
import matplotlib
matplotlib.use('Agg')

from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def main():
    m = Basemap(llcrnrlon=1, \
            llcrnrlat=40.6, \
            urcrnrlon=8.8, \
            urcrnrlat = 49.6, \
            resolution = 'l', \
            projection = 'tmerc', \
            lon_0 = 4.9, \
            lat_0 = 45.1)
    
    fig = Figure()
    canvas = FigureCanvas(fig)
    m.ax = fig.add_axes([0, 0, 1, 1])
    fig.set_figheight(8/m.aspect)
    fig.set_figwidth(8.)
    
    
    lats = [41.38, 43.18, 48.87, 43.60, 46.52, 43.28, 46.20]
    lons = [ 2.18,  3.00,  2.32,  1.43,  6.63,  5.37,  6.15]
#    name = ['Barcelona', 'Narbonne', 'Paris', 'Toulouse', 'Lausanne', 'Marseille', 'Geneva']
    
    m.drawcoastlines(color='gray')
    m.drawcountries(color='gray')
    m.fillcontinents(color='beige')
    x, y = m(lons, lats)
    m.plot(x, y, 'bo')
    canvas.print_figure('map.png', dpi=100)
    


if __name__ == '__main__':
    main()