import ogr
import sys
import os
import time as tm


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
    layer_1_sr = layer_1.GetSpatialRef()
    num_features_1 = layer_1.GetFeatureCount()
    #print num_features_1

    layer_2 = dataset_2.GetLayer(0)
    num_features_2 = layer_2.GetFeatureCount()
    #print num_features_2

    # create new .shp file for intersection
    intersect_ds = driver.CreateDataSource('ls_risk.shp')
    inter_lyr = intersect_ds.CreateLayer('bgy_ls', geom_type=ogr.wkbMultiPolygon)

    # create .prj file
    layer_1_sr.MorphToESRI()
    with open('ls_risk.prj', 'w') as f:
        f.write(layer_1_sr.ExportToWkt())

    inter_feat_defn = inter_lyr.GetLayerDefn()
    if os.path.exists('ls_risk.shp'):
        driver.DeleteDataSource('ls_risk.shp')

    # iterate thru features and create new polygon data-set out of intersections
    for j in range(num_features_2):
        feat_2 = layer_2.GetFeature(j)
        att_2 = feat_2.GetField('Rating')
        if 'High' in att_2:
            #print att_2
            geom_2 = feat_2.GetGeometryRef()
            for i in range(num_features_1):
                feat_1 = layer_1.GetFeature(i)
                geom_1 = feat_1.GetGeometryRef()
                if geom_1.Overlaps(geom_2) is True:  # check if there is overlap
                    #print 'Yes'
                    # create intersection and compute area of intersecting area
                    geom_1_area = geom_1.GetArea()
                    inter = geom_1.Intersection(geom_2)  # create intersection
                    inter_area = inter.GetArea()  # compute area of intersection
                    if (inter_area/geom_1_area) >= 0.50:
                        print inter_area/geom_1_area

                        inter_feat = ogr.Feature(inter_feat_defn)
                        inter_feat.SetGeometry(geom_1)
                        inter_lyr.CreateFeature(inter_feat)

                        # copy fields from popden layer
                        field_count = feat_1.GetFieldCount()
                        for k in range(field_count):
                            field_defn = feat_1.GetFieldDefnRef(k)
                            field_name = field_defn.GetName()
                            #inter_feat.SetField(field_name, feat_1.GetField(field_name))

                        feat_1.Destroy()

            feat_2.Destroy()

    dataset_1.Destroy()
    dataset_2.Destroy()
    intersect_ds.Destroy()

    return

def main():

    start = tm.time()

    popden = "davao_city_popden2010.shp"
    ls_susc = "dc_landslide_susct_dissolve.shp"
    risk_intersect(popden, ls_susc)

    print '\nprocessing took %f seconds' % (tm.time()-start)

if __name__=="__main__":
    main()