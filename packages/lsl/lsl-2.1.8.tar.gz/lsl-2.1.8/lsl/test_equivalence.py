#!/usr/bin/env python

from __future__ import print_function

import ephem
import lsl._skyephem as newephem

for planet in ('Sun', 'Venus', 'Jupiter', 'Saturn'):
    s0 = eval('ephem.%s()' % planet)
    s1 = eval('newephem.%s()' % planet)
    
    s0.compute()
    s1.compute()
    
    print(planet, 'a', ephem.separation((s0.a_ra,s0.a_dec), (s1.a_ra,s1.a_dec)))
    print(planet, 'g', ephem.separation((s0.g_ra,s0.g_dec), (s1.g_ra,s1.g_dec)))
    print(' ')
    
b0 = ephem.FixedBody()
b1 = newephem.FixedBody()
for attr,value in zip(('name', '_ra',           '_dec'),
                      ('CygA', '19:59:28.3566', '40:44:02.096')):
    setattr(b0, attr, value)
    setattr(b1, attr, value)

o0 = ephem.Observer()
o0.pressure = 0
o1 = newephem.Observer()
o1.pressure = 0
for attr,value in zip(('lat',        'lon',        'elev',   'date'),
                      ('34.1234324', '-108.23434', 2133.2,   '2020-03-31 00:01:02.4')):
    setattr(o0, attr, value)
    setattr(o1, attr, value)

b0.compute(o0)
b1.compute(o1)

print('fixed', 'a', ephem.separation((b0.a_ra,b0.a_dec), (b1.a_ra,b1.a_dec)))
print('fixed', 'g', ephem.separation((b0.g_ra,b0.g_dec), (b1.g_ra,b1.g_dec)))
print('fixed', 'l', ephem.separation((b0.ra,b0.dec), (b1.ra,b1.dec)))
print('fixed', 't', ephem.separation((b0.az,b0.alt), (b1.az,b1.alt)))
print('===')
print('fixed', 'nr', o0.next_rising(b0), o1.next_rising(b1))
print('fixed', 'pr', o0.previous_rising(b0), o1.previous_rising(b1))
print('fixed', 'nt', o0.next_transit(b0), o1.next_transit(b1))
print('fixed', 'pt', o0.previous_transit(b0), o1.previous_transit(b1))
print('fixed', 'ns', o0.next_setting(b0), o1.next_setting(b1))
print('fixed', 'ps', o0.previous_setting(b0), o1.previous_setting(b1))
print('fixed', 'na', o0.next_antitransit(b0), o1.next_antitransit(b1))
print('fixed', 'pa', o0.previous_antitransit(b0), o1.previous_antitransit(b1))
