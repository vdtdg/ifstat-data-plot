# ifstat-data-plot

A short python script that can be used to have a nice display of a ifstat output.
At this time, it can only support the output if you had provided the -t option on ifstat, which add timestamps to the measurements.

### Requirements
Python3, and python package *matplotlib*

### Usage
```usage: main.py [-h] [-a EMA] [-v] [-l] [input]

A python script that can be used to have a nice display of a ifstat output.

positional arguments:
   input              Output file from ifstat

optional arguments:
   -h, --help                      Show this help message and exit
   -a EMA, --ema EMA    Exponential moving average used to smooth the bandwidth. Default at 60.
   -v, --verbose                Increase output verbosity
   -l, --log                         Plot will be in logarithmic scale

Note: ifstat must be used with -t for this script to work
```