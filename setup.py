from setuptools import setup
import datetime

setup(
    name='CoAPthon3-ACME-CSE',
    version='1.1.2',
    packages=[
        'coapthon',
        'coapthon.caching',
        'coapthon.client',
        'coapthon.forward_proxy',
        'coapthon.layers',
        'coapthon.messages',
        'coapthon.resources',
        'coapthon.reverse_proxy',
        'coapthon.server'
    ],
    license='MIT License',
    author='Giacomo Tanganelli',
    author_email='giacomo.tanganelli@for.unipi.it',
    maintainer="Andreas Kraft",
    maintainer_email="an.kraft@gmail.com",
    url="https://github.com/ankraft/CoAPthon3-ACME-CSE",
    description='CoAPthon is a python library for the CoAP protocol. This fork of the library provides several updates to support the CoAP binding of the ACME oneM2M CSE',
    scripts=[
        'coapclient.py',
        'coapforwardproxy.py',
        'coapreverseproxy.py',
        'coapserver.py',
        'exampleresources.py',
    ],
    requires=['sphinx', 'cachetools']
)
