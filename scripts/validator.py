import click
import geopandas as gpd
import pandas as pd

@click.command()
@click.argument('test_polygons')
@click.argument('truth_polygons')
@click.argument('out_csv')
@click.option('--iou', '-u', type=bool, default=False,
              help="Calculate Intersect over Union?")
def main(test_polygons, truth_polygons, out_csv, iou):


    # load both files
    test_df = gpd.read_file(test_polygons)
    truth_df = gpd.read_file(truth_polygons)

    # check that crs matches
    if test_df.crs != truth_df.crs:
        raise ValueError("Input test and truth datasets do not have matching CRS.")

    # get total area of the truth data and test data
    print("Calculating total area of truth dataset")
    truth_area_km2 = truth_df.geometry.to_crs({'proj': 'cea'}).area.sum()/1e6
    print("Calculating total area of test dataset")
    test_area_km2 = test_df.geometry.to_crs({'proj': 'cea'}).area.sum() / 1e6

    # get the intersection area
    print("Calculating total area of intersection")
    intersection = gpd.overlay(test_df, truth_df, how='intersection')
    int_area_km2 = intersection.geometry.to_crs({'proj': 'cea'}).area.sum()/1e6

    # calculate statistics
    stats = dict()
    stats['recall'] = int_area_km2/truth_area_km2
    stats['precision'] = int_area_km2/test_area_km2

    if iou is True:
        # get the union area
        print("Calculating Intersect Over Union")
        union = gpd.overlay(test_df, truth_df, how='union')
        union_area_km2 = union.geometry.to_crs({'proj': 'cea'}).area.sum()/1e6
        iou = int_area_km2/union_area_km2
        stats['iou'] = iou

    # write out the results
    stats_df = pd.DataFrame([stats])
    stats_df.to_csv(out_csv, header=True, index=False)

if __name__ == '__main__':
    main()

