# nsclock
### NS (Nederlandse Spoorwegen - Dutch rail service) departure timetables for terminals and PaPiRus ePaper displays, in Python

#### nsclock.py
Prints the next up to four trains, from a configurable start point, to a configurable destination or two, on a [PaPiRus ePaper screen](https://www.pi-supply.com/?s=papirus&post_type=product&tags=1&limit=5&ixwps=1) attached to a Raspberry Pi (Zero).

![normal run](/goodies/nsclock-demo.jpg) ![exception](/goodies/nsclock-exception.jpg) 

#### nscliclock.py
Prints the same information as above to your terminal.

![normal CLI run](/goodies/nscliclock-demo.png)

##### Usage:

Step zero, [register for an NS API key](http://www.ns.nl/ews-aanvraagformulier/) (free), copy the provided settings_example.py to settings.py, and populate it with the credentials you are provided by NS. _The scripts will not work without this key._

Then, install required libraries.

```bash
pip install -r requirements.txt
```
If you are using nsclock.py, also manually install the 'papirus' library and dependencies as instructed by the documentation at https://github.com/PiSupply/PaPiRus

Then, just run in a terminal (or call with cron).
```bash
./nsclock.py
```
or
```bash
./nscliclock.py
```

The scripts are commented and contain a number of configurable variables which you can use you customize them to be useful to your own situation, e.g. start and end stations, etc.

nsclock.py requires Python 2.7, because as of 2017-07-01 there was no available LM75B temperature sensor library for Python 3, and the PaPiRus screen uses such a sensor.

### Credits
This script makes use of the NS API, documented extensively here:
http://www.ns.nl/en/travel-information/ns-api

Small pieces of code related to ePaper screen setup stolen whole from demo scripts included with PaPiRus

This was my first attempt at writing something useful in Python. I owe thanks to:

[Google](https://www.google.com/)

[stackoverflow](https://stackoverflow.com/)

[SoloLearn Python 3 course](https://www.sololearn.com/Course/Python/)