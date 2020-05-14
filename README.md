# IoT-generator-mongodb
 
__Generates bucketed IoT temperature data__

---
## Description

This script will simulate a recorded set of IoT measures (temperatures).
Each device sends a measure every minute, some measures can be missed, and measures are recording from a starting date during a number of days.

While we could save a single document for each measure, there are better ways taking advantage of the document model. In this script we are using time bucketing : each document contains up to 60 measures (1 by minute) per sensor per hour.

This kind of structure has several advantages
- lower document cardinality, meaning smaller indexes and less objects to process
- pre-calculated values (like avg, min, max) allowing for fast retrieval
- direct access to an hour of values (which makes sense if that's a use case)

A good practice is to use a bucketing method that matches best how data is consumed.

---
## Setup
* Ensure __Python 3__ is installed and install required Python libraries:
  ```bash
  pip3 install -r requirements.txt
  ```
* Edit importiot.py variables

  - startDate = datetime.datetime(2020,1,1) # first day to inject data
  - days = 140 # number of days to inject

## Run
* Get the URI for your MongoDB Setup. 

  - use "mongodb://localhost" for a local mongod
  - use "mongodb+srv://user:password@replicasetFQDN/test" format for ATLAS server (get it using "Connect" button)
  - use "mongodb://user:password@hostname" for single node remote server
etc.

* Pass the URI as a parameter :

```shell script
python3 importiot.py "mongodb+srv://user:password@replicasetFQDN/test"
```

* You can also use the docker runner if you don't want to setup the python3 environment.

```shell script
./docker-run.sh "mongodb+srv://user:password@replicasetFQDN/test"
```

## Result

The script will create a collection called `world.iot` with up to 60 measures per hour per device (so 24 documents per device per day):

```json
{
	"_id" : ObjectId("5ebc936378eac4871e4325e1"),
	"device" : "PTA101",
	"date" : ISODate("2020-01-03T00:00:00Z"),
	"unit" : "°C",
	"avg" : 19.35,
	"max" : 27.5,
	"min" : 13,
	"missed_measures" : 1,
	"recorded_measures" : 59,
	"measures" : [
		{
			"minute" : 0,
			"value" : 19
		},
		{
			"minute" : 1,
			"value" : 20.5
		},
		{
			"minute" : 2,
			"value" : 18
		},
		...
	]
}
```
