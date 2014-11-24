Scripts for McM
===============

Author: David G. Sheffield (Rutgers)

Scripts for creating and updating requests in McM. See https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVMcMScript for more information on scripts.

# Usage of manageRequests.py

Begin by getting a CERN SSO cookie with

`cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o ~/private/prod-cookie.txt --krb --reprocess`

for the production instance of McM. If you would like to test with the dev/test instance, run

`cern-get-sso-cookie -u https://cms-pdmv-dev.cern.ch/mcm/ -o ~/private/dev-cookie.txt --krb --reprocess`

If these to not work, try to run getCookie.sh. Only setup your CMSSW runtime environment after getting a cookie.

## Setup PWG

The default PWG in manageRequests.py is set to XXX. To modify your default PWG, change the variable `defaultPWG` on line 23. Alternatively, you can include the flag `-p your_PWG`.

## Creating new requests

To create new requests from a CSV file, execute the command

`python manageRequests.py -c name_of_campaign input.csv`

If you would like to create new requests by cloning an existing request, execute the command

`python manageRequests.py --clone PrepId_of_request_to_clone input.csv`

Unless the flags `--clone` or `--modify` or `-m` are used, the script will use the CSV file to create new requests from scratch.

## Modifying existing requests

To modify an existing request, execute the command

`python manageRequests.py -m input.csv`

The CSV file must contain the PrepIds of the requests to modify.

## CSV file

Information for requests is provided in a CSV file. The script reads the first line of the file for the names of fields:

* Dataset name
* Total events
* Cross section [pb]
* Time per event [s]
* Size per event [kB]
* Fragment tag
* Generator
* EOS
* Filter efficiency
* Filter efficiency error
* Match efficiency
* Match efficiency error
* PWG
* Campaign
* PrepId

It will also recognize some alternative names. If there is a field title that the script does not recognize, it will complain.

To add multiple generators per requests, separate them with a space.

The campaign and PWG can also be given for all requests with the flags `-c` and `-p`, respectively. If the PWG is neither given in the command line nor the CSV file, it will take its default value.

The field PrepId is only used in modifying requests, where it is required.

## Dry run

The input.csv file can be tested with a dry run using the flag `-d`. Additionally, you can submit to the dev/test instance of McM using the flag `--dev`.

# Usage of getTimeSize.sh

After running

`cmsrun -e -j log.xml test_cfg.py`

to measure the time and size of a request, you can extract the time per event and calculate the size per event in kilobytes by running

`sh getTimeSize.sh log.xml`
