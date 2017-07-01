# nsclock
### NS (Nederlandse Spoorwegen - Dutch rail service) departure timetables in Python

#### nsclock.py
Prints the next up to four trains, from a configurable start point, to a configurable destination or two, on a PaPiRus ePaper screen attached to a Raspberry Pi (Zero).

![normal run](/goodies/nsclock-demo.jpg) ![exception](/goodies/nsclock-exception.jpg) 

#### nscliclock.py
Prints the same information as above to your terminal.

![normal CLI run](/goodies/nscliclock-demo.png)

##### Usage:

```bash
pip install -r requirements.txt
```

If you are using nsclock.py, also manually install the 'papirus' library and dependencies as instructed by the documentation at https://github.com/PiSupply/PaPiRus

```bash
./nsclock.py

or

./nscliclock.py
```

The scripts are commented and contain a number of configurable variables which you can use you customize them to be useful to your own situation, e.g. start and end stations, etc.

nsclock.py requires Python 2.7 because as of 2017-07-01 there was no available LM75B temperature sensor library for Python 3, and the PaPiRus screen uses such a sensor.