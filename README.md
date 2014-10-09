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
