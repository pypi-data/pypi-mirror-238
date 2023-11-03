=============
epconversions
=============


.. image:: https://img.shields.io/pypi/v/epconversions.svg
        :target: https://pypi.python.org/pypi/epconversions

.. image:: https://img.shields.io/travis/pyenergyplus/epconversions.svg
        :target: https://travis-ci.com/pyenergyplus/epconversions

.. image:: https://readthedocs.org/projects/epconversions/badge/?version=latest
        :target: https://epconversions.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/pyenergyplus/epconversions/shield.svg
     :target: https://pyup.io/repos/github/pyenergyplus/epconversions/
     :alt: Updates



Unit conversions for E+


* Free software: Mozilla Public License 2.0 (MPL 2.0)
* Documentation: https://epconversions.readthedocs.io.


Energyplus has a bunch of conversion factors at the top of the `Energy+.idd` file. It looks like this::

    ! Default IP conversions (no \ip-units necessary)
    !      $/(m3/s)               =>   $/(ft3/min)         0.000472000059660808
    !      $/(W/K)                =>   $/(Btu/h-F)         0.52667614683731
    !      $/kW                   =>   $/(kBtuh/h)         0.293083235638921
    !      $/m2                   =>   $/ft2               0.0928939733269818
    !      $/m3                   =>   $/ft3               0.0283127014102352
    !      (kg/s)/W               =>   (lbm/sec)/(Btu/hr)  0.646078115385742
    !      1/K                    =>   1/F                 0.555555555555556
    !      1/m                    =>   1/ft                0.3048
    !      A/K                    =>   A/F                 0.555555555555556
    !      C                      =>   F                   1.8 (plus 32)
    !      cm                     =>   in                  0.3937
    !      cm2                    =>   inch2               0.15500031000062
    !      deltaC                 =>   deltaF              1.8
    !      deltaC/hr              =>   deltaF/hr           1.8
    !      deltaJ/kg              =>   deltaBtu/lb         0.0004299
    !      g/GJ                   =>   lb/MWh              0.00793664091373665
    !      g/kg                   =>   grains/lb           7

Note the `cm` in the middle of that text snippet. It shows the conversion form `cm` to `in` and the multipier to use to convert





Features
--------

The library `epconversions` has functions that will do these conversions::

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


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
