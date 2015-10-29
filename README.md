
ilastikDiagnosticTools
============

A collection of tools to profile and optimize ilastik's running-time.

Features
--------

* A parameter-optimization script `src/paramOpt.py` that runs cross-validation tests to find the optimal number of trees and features.
* A simple test script `src/runningTimeProf.py` that isolates feature computation and prediction in order to profile the time for each of these stages individually.
* A script `trackingCsvDiagnostics.py` to read and diagnose the conservation-tracking csv result files.


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

Instructions to Run the Profiling Script
---------------------------------------

The file `trackingCsvDiagnostics.py` allows the user to plot different tracking parameters contained in the csv files. Here's a list of the arguments available.

  | Argument | Description |
  | --- | --- | --- |
  | -h, --help |           show this help message and exit |
  | --file FILE |          Name of conservation-tracking csv file. |
  | --lineage-ids |        Plot the lineage IDs. |
  | --tracks |             Plot the tracks of all the objects in the file. |
  | --object-num |         Plot the number of objects per frame. |
  | --errors |             Plot the errors per frame. These errors include appearing IDs and repeated IDs. |
  | --collisions |         Plot the number of collisions per frame. |
  | --bounding-rect BOUNDINGRECT | Plot the bounding rectangles for the choose frame. |

1. Download and install the latest versions of ilastik and lazyflow.
2. Run the tracking diagnostics script with the tests csv file with the following command:

`>>>python trackingCsvDiagnostics.py`

