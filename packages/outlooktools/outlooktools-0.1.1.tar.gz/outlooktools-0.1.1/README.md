# OutlookTools

[![PyPI - Version](https://img.shields.io/pypi/v/outlooktools.svg)](https://pypi.org/project/outlooktools)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/outlooktools.svg)](https://pypi.org/project/outlooktools)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install outlooktools
```

## License

`outlooktools` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

# OutlookTools
 Windows CLI tool to automate some Outlook activities.

 Works via MAPI interface to the user's Outlook session.

 Only works on Windows systems

 Current functions:
 - List mailboxes
 - List folders
 - Save all attachments found in a given folder to a given location
 - Send a plain text email (as the current user) with an attachment as desired.

 When installed should put a "OutlookTools.exe" on your path so can run from the command line

 The MAPI interface can do A LOT.  Basically anything you can do with VBA as described [here:](https://learn.microsoft.com/en-us/office/vba/api/overview/outlook)
 
 Have fun extending
