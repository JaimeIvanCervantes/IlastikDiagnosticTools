
ilastik-prof
============

A collection of tools to profile and optimize ilastik's running time.

Features
--------
* A simple test script to profile ilastik feature computation and prediction running times.
* A script to find the optimal number of trees and parameters.

Instructions
------------
1. Download the latest versions of ilastik and lazyflow.
2. Run the feature optimization script with the following command:
`python prof.py --run_command=<ilastik-run-command> --data_file=<hdf5-data-file> --project_file=<ilp-project-file> --features_test --trees_test`
