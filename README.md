Scripts for McM
===============

Author: David G. Sheffield (Rutgers)

Scripts for creating and updating requests in McM. See https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVMcMScript for more information on scripts.

# Usage

Begin by getting a CERN SSO cookie with

`cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o ~/private/cookie.txt --krb --reprocess`

Then setup your CMSSW runtime environment before proceeding.