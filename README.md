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

The CSV file must contain the PrepIds of the requests to modify. If the CSV file contains dataset names, adding the flag `-l` will only modify the request if the request's dataset name matches that in the CSV file.

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
* Sequences customise
* Process string
* Gridpack location
* Gridpack cards URL

It will also recognize some alternative names. If there is a field title that the script does not recognize, it will complain.

To add multiple generators per requests, separate them with a space.

The campaign and PWG can also be given for all requests with the flags `-c` and `-p`, respectively. If the PWG is neither given in the command line nor the CSV file, it will take its default value.

The field PrepId is only used in modifying requests, where it is required.

## Dry run

The input.csv file can be tested with a dry run using the flag `-d`. Additionally, you can submit to the dev/test instance of McM using the flag `--dev`.

# Usage of testRequests.py

This script will submit lxbatch jobs to test requests and chained requests. It creates a CSV file when tests are submitted that contains the PrepIDs and lxbatch job ID of every request. Chained requests will have separate entries for the chained request's wmLHE request and GS request with a shared job ID. When the batch jobs finish, `testRequests.py` can be run again to update the CSV file to include the time and size per event. This CSV file can be used with `manageRequests.py` to add the time and size per event to McM.

## Creating tests

If you are testing a chained request, you must first get a CERN SSO cookie to access McM to get the chained request's component request PrepIDs. No other operations require that.

Create a test of requests with the command

`python testRequests.py -i PrepIDList`

Nonconsecutive PrepIDs can be separated by a comma `,` while ranges can be specified by a dash `-`. The final request in a range can either be specified with its full PrepID (in which case, the PWG and campaign must match that of the first PrepID) or just the numbercan be used. The following command will test seven requests from two campaigns:

`python testRequests.py -i EXO-RunIIWinter15GS-00001,EXO-RunIIWinter15GS-00003-EXO-RunIIWinter15GS-00005,EXO-chain_RunIIWinter15wmLHE_flowRunIIWinter15wmLHEtoGS-00002-4`

The output CSV file can be specified with the flag `-o file.csv`. The default filename is `test.csv`.The number of events tested will be McM's default. To use N events for all tests, add the flag `-n N`.

## Extracting test results

To extract the time and size per event from the tests, run the command

`python testRequests.py -f file.csv`

on the file created when the tests were submitted.

The script will extract the average time and size of events and store it in the CSV file. If `testRequests.py` is run before all batch jobs finish, it will tell you how many requests still need to have their information filled. The script can be run any number of times to update the remaining requests.

# Usage of validateChains.py

To validate multiple chained requests in McM run the command

`python validateChains.py firstPrepID lastPrepID`

The script will tell McM to validate all requests with PrepIDs within that range.

# Usage of getMcMTestScript.sh

The command

`sh getMcMTestScript PrepID`

will get the request's test script from McM and store it in test.sh. Run `sh test.sh` to execute the test locally. The output file can be modified by the flag `-o` and the number of events can be modified using the flag `-n`.

# Usage of getTimeSize.sh

After running

`cmsrun -e -j log.xml test_cfg.py`

to measure the time and size of a request, you can extract the time per event and calculate the size per event in kilobytes by running

`sh getTimeSize.sh log.xml`
