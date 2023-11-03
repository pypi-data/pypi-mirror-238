# -*- coding: utf-8 -*-
__author__ = "Peter Gastinger"
__copyright__ = "Copyright 2023, OMV"
__credits__ = ["Peter Gastinger"]
__license__ = "GPL"
__version__ = "0.2"
__maintainer__ = "Peter Gastinger"
__email__ = "peter.gastinger@omv.at"
__status__ = "Production"

# REST SDK
# https://campus.barracuda.com/product/cloudgenfirewall/api/8.3
#
# tested with 8.0.4 and 8.3.1


class BarracudaEntryAlreadyExistsException(Exception):
    pass


class BarracudaEntryNotFoundException(Exception):
    pass
