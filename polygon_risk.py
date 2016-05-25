import ogr
import sys
import os

def risk_intersect(ds1, ds2):
    driver = ogr.GetDriverByName('ESRI Shapefile')

    dataset_1 = driver.Open(ds1)
    if dataset_1 is None:
        print 'Could not open' + dataset_1
        sys.exit(1)

    dataset_2 = driver.Open(ds2)
    if dataset_2 is None:
        print 'Could not open' + dataset_2
        sys.exit(1)

    layer_1 = dataset_1.GetLayer(0)
    num_features_1 = layer_1.GetFeatureCount()
    print num_features_1

    layer_2 = dataset_2.GetLayer(0)
    num_features_2 = layer_2.GetFeatureCount()
    print num_features_2

    # create new .shp file for intersection
    intersect_ds = driver.CreateDataSource('ls_risk.shp')
    inter_lyr = intersect_ds.CreateLayer('bgy_ls', geom_type=ogr.wkbMultiPolygon)
    if os.path.exists('ls_risk.shp'):
        driver.DeleteDataSource('test.shp')

    # iterate thru features and create new polygon data-set out of intersections
    for j in range(num_features_2):
        feat_2 = layer_2.GetFeature(j)
        att_2 = feat_2.GetField('Rating')
        if 'High' in att_2:
            print att_2
            geom_2 = feat_2.GetGeometryRef()
            for i in range(num_features_1):
                feat_1 = layer_1.GetFeature(i)
                geom_1 = feat_1.GetGeometryRef()
                if geom_1.Overlaps(geom_2) is True: # check if there is overlap
                    print 'Yes'
                    # create new features out of intersection
                    inter = geom_1.Intersection(geom_2) # create intersection
                    bgy_name_defn = feat_1.GetFieldDefnRef('NAME_3')
                    pop_den = feat_1.GetField




    return

def main():
    popden = "davao_city_popden2010.shp"
    ls_susc = "dc_landslide_susct_dissolve.shp"
    risk_intersect(popden, ls_susc)

if __name__=="__main__":
    main()