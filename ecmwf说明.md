# Introduction

This is a brief introduction of the main request parameter syntax.
We recommend that you get familiar with datasets and their availability using [http://apps.ecmwf.int/datasets/](http://apps.ecmwf.int/datasets/)

You can also get the request syntax using **"View MARS request"**feature.

# Syntax

verb,

keyword1 = value1,
... = value2,

keywordN = valueN

* verb: action to be taken (e.g. retrieve, list, read)
* keyword: a known MARS variable, e.g. type or date
* value: value assigned to the keyword, e.g. Analysis or temperature

Retrieve example from "View MARS request":
**MARS request**
retrieve,
stream=oper,
levtype=sfc,
param=165.128/41.128,
dataset=interim,
step=0,
grid=0.75/0.75,
time=00,
date=2013-09-01/to/2013-09-30,
type=an,
class=ei
**Python equivalence**
/#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
server=ECMWFDataServer()

server.retrieve({
'dataset':"interim",
'time':"00",
'date':"2013-09-01/to/2013-09-30",
'step':"0",
'type':"an",
'levtype':"sfc",
'param':"165.128/41.128",
'grid':"0.75/0.75",
'target':"interim201309.grib"
})

# Keyword

In the Dataset service there is an extra mandatory keyword called **dataset** which does not appear in normal MARS requests.
KeyworddefinitiondatasetSee[Available Datasets](https://confluence.ecmwf.int/display/WEBAPI/Available+ECMWF+Public+Datasets)formatYou can add **'format' : "netcdf"** to retrieve the data in NetCDF format.

the other possible MARS keywords are explained in the [Legacy MARS keywords](https://confluence.ecmwf.int/display/UDOC/Legacy+MARS+keywords) documentation.

[](https://confluence.ecmwf.int/display/WEBAPI/Brief+request+syntax)