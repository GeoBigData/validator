import os
import json
import glob
import validator


def convert_type(var, f, expected_type):

    # try to convert the inputs to correct types
    if var is None:
        return None

    if f == bool:
        if var.lower() == 'true':
            return True
        else:
            return False
    else:
        try:
            var = f(var)
        except ValueError as e:
            err = "Inputs {var} cannot be converted to type {expected_type}".format(var=var,
                                                                                    expected_type=expected_type)
            raise ValueError(err)

        return var


def main():

    # get the inputs
    input_truth = '/mnt/work/input/truth'
    input_test = '/mnt/work/input/test'
    string_ports = '/mnt/work/input/ports.json'

    # create output directory
    out_path = '/mnt/work/output/data'
    if os.path.exists(out_path) is False:
        os.makedirs(out_path)

    # read the inputs
    with open(string_ports) as ports:
        inputs = json.load(ports)
    iou = inputs.get('iou', 'False')
    out_csv = inputs.get('out_csv', 'results.csv')

    # convert the inputs to the correct dtypes
    iou = convert_type(iou, bool, 'Boolean')
    out_csv = convert_type(out_csv, str, 'String')

    # get the shp or geojson in the input truth folder
    truth_vectors = glob.glob1(input_truth, '*.shp')
    truth_vectors += glob.glob1(input_truth, '*.geojson')
    if len(truth_vectors) == 0:
        raise ValueError("No shp or geojson files found in input data port 'truth'")
    if len(truth_vectors) > 1:
        raise ValueError("Multiple shp or geojson found in input data port 'truth'")
    in_truth = os.path.join(input_truth, truth_vectors[0])

    # get the shp or geojson in the input test folder
    test_vectors = glob.glob1(input_test, '*.shp')
    test_vectors += glob.glob1(input_test, '*.geojson')
    if len(test_vectors) == 0:
        raise ValueError("No shp or geojson files found in input data port 'test'")
    if len(test_vectors) > 1:
        raise ValueError("Multiple shp or geojson found in input data port 'test'")
    in_test = os.path.join(input_test, test_vectors[0])

    # set the output file path
    out = os.path.join(out_path, out_csv)

    print("Validating test data against truth data...")
    # run the processing
    validator.main([in_test,
                    in_truth,
                    out,
                    '-u', iou])
    print("Validation process completed successfully.")

if __name__ == '__main__':
    main()
