from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def main():
    # setup Lambert Conformal basemap.
    w = 5000000
    m = Basemap( width=w
                ,height=w
                ,projection='tmerc'
                ,resolution='i'
                ,lat_1=-15.5
                ,lat_2=-15
                ,lat_0=-14.5
                ,lon_0=-55.
            )
    # draw coastlines.
#    m.drawcoastlines()
    # draw a boundary around the map, fill the background.
    # this background will end up being the ocean color, since
    # the continents will be drawn on top.
    m.drawmapboundary(fill_color='aqua') 
    # fill continents, set lake color same as ocean color. 
    m.fillcontinents(color='gray',lake_color='aqua')
    m.drawstates(linewidth=.5)
    m.drawcountries(linewidth=1.5)
    plt.savefig('background3.png')

if __name__ == '__main__':
    main()