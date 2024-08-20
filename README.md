
# CoAPthon3
CoAPthon3 is a porting to python3 of my CoAPthon library. CoAPthon3 is a python3 library to the CoAP protocol compliant with the RFC. Branch is available for the Twisted framework.

# ACME oneM2M CSE Fork

This fork of CoAPthon3 corrects some issues with the original library and adds further functionality to support the [ACME oneM2M CSE](https://https://github.com/ankraft/ACME-oneM2M-CSE) project.

The changes mainly include:

- Add the possibility to add own options and content types to the library.
- Fixes issues when sending and receiving large responses in blockwise mode.
- Improve the means to add an own request layer. The original implementation mainly supports pre-registered resources, which is is difficult to the way oneM2M resources work.

## Installation

To install the library, you can use the following command:

```bash
pip install CoAPthon3-ACME-CSE
```
