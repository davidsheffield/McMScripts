Scripts for McM
===============

Author: David G. Sheffield (Rutgers)

Scripts for creating and updating requests in McM. See https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVMcMScript for more information on scripts.

# Usage

Begin by getting a CERN SSO cookie with

`cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o ~/private/cookie.txt --krb --reprocess`

for the production instance of McM. If you would like to test with the dev/test instance, run

`cern-get-sso-cookie -u https://cms-pdmv-dev.cern.ch/mcm/ -o ~/private/cookie.txt --krb --reprocess`

Then setup your CMSSW runtime environment before proceeding.

## Setup PWG

The default PWG in create.py is set to XXX. To modify your default PWG, change the variable `defaultPWG` on line 11. Alternatively, you can include the `-p your_PWG`.

## Creating new requests

To create new requests from a CSV file, execute the command

`python create.py -c name_of_campaign input.csv`

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

It will also recognize some alternative names. If there is a field title that the script does not recognize, it will complain.

To add multiple generators per requests, separate them with a space.

The campaign and PWG can also be given for all requests with the flags `-c` and `-p`, respectively. If the PWG is neither given in the command line nor the CSV file, it will take its default value.

## Dry run

The input.csv file can be tested with a dry run using the flag `-d`. Additionally, you can submit to the dev/test instance of McM using the flag `--dev`.
