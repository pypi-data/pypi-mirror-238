import lsl._skyephem as ephem
import coordinates as co
from dates import J2000, B1950

e = ephem.Equatorial(ephem.hours(1.0), ephem.degrees(0.5), epoch=ephem.J2000)
c = co.Equatorial(1.0, 0.5, epoch=J2000)
print(e.ra, c.ra)
e = ephem.Equatorial(e, epoch=ephem.B1950)
c = co.Equatorial(c, epoch=B1950)
print(e.ra, c.ra)
e = ephem.Galactic(e, epoch=ephem.B1950)
c = co.Galactic(c, epoch=B1950)
print(e.lat, c.lat)
e = ephem.Ecliptic(e, epoch=ephem.J2000)
c = co.Ecliptic(c, epoch=J2000)
print(e.lat, c.lat)
