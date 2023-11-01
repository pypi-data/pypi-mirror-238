================
Unglue It Driver
================

Driver to retrieve metrics from the Unglue.it portal.

Refer to https://unglue.it/api/help to get the api key from.

Code for the HIRMEOS project is available at https://github.com/hirmeos/unglueit_driver.

For more information about the OPERAS metrics, go to
https://metrics.operas-eu.org/


Troubleshooting
===============

At the moment of testing the plugin, despite doing 3 get requests to the API to get
the needed dataset it wasn't slow enough to be a concern but an improvement to the
API would be great making less calls and a filter by date would be a preference.

Another improvement straight away related to the package would be adding the rest of
identifiers from the dataset returned ('goog' and 'oclc') if they are needed in the future.

Release Notes:
==============

[0.0.1] - 2023-10-27
---------------------
Added
.......
    - Logic to initialise the Unglue.it driver