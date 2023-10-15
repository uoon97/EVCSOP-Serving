# Serving for EV Charger Station Occupancy Prediction Model

Repo for serving EV charger station occupancy prediction models using aws EC2 and Lambda Respectively.
Original Repo: https://github.com/easttuna/ev-charger-occupancy-prediction


The required input features are as follows.

Station
- Station id : dims = (1,)
- number of chargers(slow/fast) : dims = (2,)
- supply capacity : dims = (1,)
- location of station(lat/lon) : dims = (2,)
- average of taxi trip of road link within 500m radius : dims = (1,)
- proportion of road type within 500m radius(4 road type) : dims = (4,)
- proportion of district type within 500m radius(5 district type) : dims = (5,)

Sequence
- Realtime Sequence : dims = (12, 1)
- Historical Sequence : dims = (4, 1)

Time
- (Time Index, day of week, weekday) : dims = (3,)

<br>

Outputs are as follows.

- Occupancy_20, 40, 60, 120 / continuous : dims = (4, 1)

<br>


