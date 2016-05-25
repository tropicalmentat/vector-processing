import ogr
import sys

def risk_intersect(ds1, ds2):
    driver = ogr.GetDriverByName('ESRI Shapefile')

    dataset_1 = driver.Open(ds1)
    if dataset_1 is None:
        print 'Could not open' + fn
        sys.exit(1)

    layer_1 = dataset_1.GetLayer(0)
    num_features_1 = layer_1.GetFeatureCount()
    print num_features_1

    dataset_2 = driver.Open(ds2)
    if dataset_2 is None:
        print 'Could not open' + fn
        sys.exit(1)

    layer_2 = dataset_2.GetLayer(0)
    num_features_2 = layer_2.GetFeatureCount()
    print num_features_2

    return

def main():
    popden = "davao_city_popden2010.shp"
    ls_susc = "dc_landslide_susct.shp"
    risk_intersect(popden, ls_susc)

if __name__=="__main__":
    main()