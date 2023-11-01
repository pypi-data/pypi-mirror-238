import lsl._skyephem as ephem
import observers
import satellites

d = ephem.city('Dallas')
d.date = '2019/12/30 00:00:00'
d.pressure = 0.0

obs = observers.Observer()
obs.lat = d.lat
obs.lon = d.lon
obs.elev = d.elev
obs.date = d.date

tle = ['ISS (ZARYA)  ',
       '1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991',
       '2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482']

e = ephem.readtle(*tle)
s = satellites.readtle(*tle)

e.compute(d)
print(e.ra, e.dec)
s.compute(obs)
print(s.ra, s.dec)
