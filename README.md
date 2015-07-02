# sens-o-matic
Triggering scenarios on sensors activation

## First run

Create tables in database with::

    $ python -m sensomatic.ui.persistence.models

Then run sens-o-matic with::

    $ python main.py

## Sources
Classes that provide iterable objects for retrieving information from different sources.
See implemented example weather.

## Sensors
Sensor is Observable objects factory, it should provide only one Observable for every kind of sensor.
E.g. every separate sensor will be singleton. For Weather example it provides singleton Observable object
 for every separate city.
