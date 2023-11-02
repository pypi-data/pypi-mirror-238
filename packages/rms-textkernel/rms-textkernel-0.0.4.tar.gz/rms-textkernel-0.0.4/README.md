| PyPI Release | Test Status | Code Coverage |
| ------------ | ----------- | ------------- |
| [![PyPI version](https://badge.fury.io/py/rms-textkernel.svg)](https://badge.fury.io/py/rms-textkernel) | [![Build status](https://img.shields.io/github/actions/workflow/status/SETI/rms-textkernel/run-tests.yml?branch=master)](https://github.com/SETI/rms-textkernel/actions) | [![Code coverage](https://img.shields.io/codecov/c/github/SETI/rms-textkernel/main?logo=codecov)](https://codecov.io/gh/SETI/rms-textkernel) |

# rms-textkernel

PDS Ring-Moon Systems Node, SETI Institute

Supported versions: Python >= 3.7

This is a set of routines for parsing SPICE text kernels. It returns a
dictionary of all the parameters and their values. It implements the complete
syntax specification as discussed in the SPICE Kernel Required Reading
document, "kernel.req". However, it cannot be guaranteed that the parsing of
date/time fields is identical, although dates that are unambiguous should be
treated the same.

Method:
  textkernel.FromFile(filename, clear=True)

```
Input:
  filename        the name of a text file.
  clear           True to return the contents of this text kernel only;
                  False to return a dictionary in which the contents of the
                  prior call(s) to FromFile() have been merged with the new
                  entries.

Return:           A dictionary.
```

Note that the returned dictionary is keyed in a very specific way based on the
structure of the keyword names in the kernel. Examples:

```
  BODY399_POLE_RA     dict["BODY"][399]["POLE_RA"]
  MESSAGE             dict["MESSAGE"]
  DELTET/EB           dict["DELTET"]["EB"]
  FRAME_624_NAME      dict["FRAME"][624]["NAME"]
```

Also, frames and bodies can be referenced by their name or their numeric ID.
These are equivalent:

```
  dict["FRAME"][623]      dict["FRAME"]["IAU_SUTTUNGR"]
  dict["BODY"][399]       dict["BODY"]["SATURN"]
```

Frame and body dictionaries also have an additional keyword "ID" added, which
returns the numeric ID and is useful when the dictionary is selected by name
instead. Example:

```
  dict["FRAME"]["IAU_SUTTUNGR"]["ID"] = 623
  dict["FRAME"][623]["ID"] = 623
```
