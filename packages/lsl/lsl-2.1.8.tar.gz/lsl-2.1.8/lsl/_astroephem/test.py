import observers
import bodies
import lsl._astroephem as ephem

d = ephem.city('Dallas')
d.pressure = 0.0

obs = observers.Observer()
obs.lat = d.lat
obs.lon = d.lon
obs.elev = d.elev
obs.date = d.date
print(d.date, obs.date)

e = ephem.Sun()
e.compute(d)
print(e.az, e.alt, e.a_dec, e.g_dec, e.dec)

s = bodies.Sun()
s.compute(obs)
print(s.az, s.alt, s.a_dec, s.g_dec, s.dec)

t = d.previous_transit(e)
print(t*1.0)
t = obs.previous_transit(s)
print(t*1.0)
