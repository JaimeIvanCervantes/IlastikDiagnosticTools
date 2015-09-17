
ilastik-prof
============

A collection of tools to profile and optimize ilastik's running-time.

Features
--------

* A parameter-optimization script `src/paramOpt.py` that runs cross-validation tests to find the optimal number of trees and features.
* A simple test script `src/runningTimeProf.py` that isolates feature computation and prediction in order to profile the time for each of these stages individually.


Instructions to Run the Parameter-Optimization Script
-----------------------------------------------------

1. Download and install the latest versions of ilastik and lazyflow.
2. IMPORTANT: Change directory to the parent folder that contains the project (.ilp) file.
3. Run the parameter-optimization script with the following command:

`>>>python paramOpt.py --run_command=<ilastik-run-command> --project-file=<ilp-project-file>`

Instructions to Run the Profiling Script
---------------------------------------
1. Download and install the latest versions of ilastik and lazyflow.
2. Run the profiling script with the following command:

`>>>python runningTimeProf.py <project-file> <data-file> <threads-enabled> <thread-number>`
