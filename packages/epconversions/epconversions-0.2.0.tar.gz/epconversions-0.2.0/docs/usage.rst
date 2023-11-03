=====
Usage
=====

To use epconversions in a project::

    from epconversions import epconversions
    print(epconversions.convert2ip(100, 'cm'))
    >> (39.37, 'in')

Can I convert to SI units ? Yes.::

    epconversions.convert2si(100, 'in')
    >> (254.00050800101602, 'cm')

What if I want only converted value. I don't want the unit string::

    epconversions.convert2si(100, 'in', unitstr=False)
    >> 254.00050800101602

Nice !!

Why does it convert ``cm`` to ``in``. Would it convert to ``m``::

    epconversions.convert2si(100, 'in', 'm')
    >> (2.5399999999999987, 'm')

    # for clarity
    epconversions.convert2si(100, 'in', siunit='m')
    (2.5399999999999987, 'm')


What are all the units it can convert ``in`` to ?::

    epconversions.getsiunits('in')
    >> {'cm', 'm'}

How do I know what it converts it to by default?::

    epconversions.defaultsiunit('in')
    >> 'cm'
    epconversions.defaultsiunit('ft')
    >> 'm'

What are all the units it can convert?::

    epconversions.allsiunits()
    >> ['$/(m3/s)',
    '$/(W/K)',

    <snip>

    'A/K',
    'C',
    'cm',
    'cm2',
    'deltaC',
    'deltaC/hr',
    'deltaJ/kg',
    'g/GJ',
    'g/kg',
    'g/MJ',


    <snip>

    'W',
    'W/((m3/s)-Pa)',
    'W/(m3/s)',
    'W/K',
    'W/m',
    'W/m2',

    <snip>

    'years']

    # around 128 now

    # also try out ``allipunits()``


Thats all for now

