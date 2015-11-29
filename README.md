Scripts for McM
===============

Author: David G. Sheffield (Rutgers), extension of getRequests.py by Luca Perrozzi (ETHZ)

Scripts for creating and updating requests in McM. See https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVMcMScript for more information on scripts.

Scripts
-------

* [**manageRequests.py**](#usage-of-managerequestspy) Create, modify, and clone requests in McM.
* [**getRequests.py**](#usage-of-getrequestspy) Get formatted list of requests from McM that can be used by other scripts.
* [**testRequests.py**](#usage-of-testrequestspy) Test time/size per event of requests using batch jobs.
* [**validateChains.py**](#usage-of-validatechainspy) Validate list of chained requests.
* [**checkRequests.py**](#usage-of-checkrequestspy) Check the status of requests and those chained to them.
* [**copyGridpacks.sh**](#usage-of-copygridpackssh) Copy gridpacks to EOS.
* [**copyPrivateLHEs.sh**](#usage-of-copyprivatelhessh) Copy LHE files to EOS.
* [**getMcMTestScript.sh**](#usage-of-getmcmtestscriptsh) Get test script from McM with some modifications.
* [**getTimeSize.sh**](#usage-of-gettimesizesh) Extract time/size per event from cmsRun job report.

Get cookies
-----------

Some scripts require getting a CERN SSO cookie before using them. They can be obtained for the production instance of McM with

`cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o ~/private/prod-cookie.txt --krb --reprocess`

and for the dev/test instance with

`cern-get-sso-cookie -u https://cms-pdmv-dev.cern.ch/mcm/ -o ~/private/dev-cookie.txt --krb --reprocess`

Run these commands before setting up a CMSSW environment. If these to not work, try to run [getCookie.sh](getCookie.sh).

Format of PrepID lists
----------------------

Several scripts use lists of PrepIDs. Multiple requests can be seperated by a `,` as in

`EXO-RunIIWinter15GS-00001,EXO-RunIIWinter15GS-00003`

Consecutive requests can be expressed as ranges separated by `-`. The PWG and campaign must be the same for both the first and last PrepID. Alternatively, the PWG and campaign can be omitted. For example, here is a list of five requests:

`HIG-Fall13pLHE-00027-HIG-Fall13pLHE-00028,TOP-chain_RunIIWinter15GS_flowRunIISpring15DR74Startup25ns-00001-3`

Adding scripts to path
----------------------

To make the scripts available from your working area, you can either create symbolic links from `~/scripts/` to these scripts or add this directory to your path. You also will be able to run the scripts without writing `python` or `sh`.


Usage of manageRequests.py
--------------------------

[manageRequests.py](manageRequests.py) handles batch creation, modification, and cloning of scripts based on the contents of a CSV file. Requires you to [get cookies](#get-cookies) before beginning.

### Setup PWG

The default PWG in manageRequests.py is set to XXX. To modify your default PWG, change the variable `defaultPWG` on line 23. Alternatively, you can include the flag `-p your_PWG`.

### Creating new requests

To create new requests from a CSV file, execute the command

`python manageRequests.py -c name_of_campaign input.csv`

If you would like to create new requests by cloning an existing request, execute the command

`python manageRequests.py --clone PrepId_of_request_to_clone input.csv`

Unless the flags `--clone` or `--modify` or `-m` are used, the script will use the CSV file to create new requests from scratch.

### Modifying existing requests

To modify an existing request, execute the command

`python manageRequests.py -m input.csv`

The CSV file must contain the PrepIds of the requests to modify unless the `-l` flag is used. To modify existing requests based on dataset names (helpful for modifying GS requests chained from pLHE and wmLHE ones), use the `-l` flag

`python manageRequests.py -m -l -c name_of_campaign input.csv`

where the CSV file contains the dataset names. It will search for requests that match the dataset name and campaign then modify the other fields if it finds the requests.

### CSV file

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
* Notes

It will also recognize some alternative names. If there is a field title that the script does not recognize, it will complain. The script will ignore columns with the headers "JobId", "Local gridpack location", and "Local LHE" as they are used to supply information to other scripts but do not contain information for McM.

To add multiple generators per requests, separate them with a space (e.g., "madgraph pythia8").

The campaign and PWG can also be given for all requests with the flags `-c` and `-p`, respectively. If the PWG is neither given in the command line nor the CSV file, it will take its default value.

The field PrepId is only used in modifying requests.

Adding the fields "Gridpack location" and "Gridpack cards URL" will generate a LHEProducer fragment.

### Dry run

The input.csv file can be tested with a dry run using the flag `-d`. Additionally, you can submit to the dev/test instance of McM using the flag `--dev`.

Usage of getRequests.py
-----------------------

[getRequests.py](getRequests.py) takes gets requests from McM based on a query and extracts their PrepIDs. Requires you to [get cookies](#get-cookies) before beginning. To get all SUS requests from RunIISummer15GS in status new and not being validated, execute the command

`python getRequests.py "pwg=SUS&member_of_campaign=RunIISummer15GS&status=new&approval=none"`

Use quotation marks when joining multiple fields with `&`. This will return a list of PrepIDs formatted to be used by other scripts. It will also count the number of requests and give you the total number of events.

The formatting can be changed with the flag `-f`. The default is `-f 0`, which will [properly format](#format-of-prepid-lists) the list for other scripts like [testRequests.py](testRequests.py). The option `-f 1` will make the lists human readable with ranges separated by `--->` and spaces added in between PrepIDs. Using `-f 2` will separate requests that are not ranges with `<br>` so that they appear on separate lines on a twiki.

The script can sort for only requests with time per event and size per event set to -1 with `-n` (e.g., to find requests to test). It can sort for requests with positive time/size per event with `-v` (e.g., to find requests ready for validation).

To obtain a list of chained requests from wmLHE requests you can use the `-c` flag.

NEW: a new funcionality has been added to dump much more information (with COLORS!), to be launched with the flag '--listattr'. The default is `-f 0` (Dataset name, Extension, Number of Completed/Total events). The level of verbosity can be increased to `-f 1` (Status, Time Event, CMSSW Release, Priority), `-f 2` (Cross Section, Filter efficiency, Matching efficiency, Tags, Generators, Name of Fragment, Notes), `-f 3` (Last Updater Name and Email, McM View and Edit Links), `-f 4` (Member of the chains including prepIds of the chained requests and direct McM chain link), and `-f 5` (Fragment code). Example:

`python getRequests.py -listattr 5 "actor=perrozzi&member_of_campaign=*GS*&status=new"`

Usage of testRequests.py
------------------------

[testRequests.py](testRequests.py) submits lxbatch jobs to test requests and chained requests. It creates a CSV file when tests are submitted that contains the PrepIDs and lxbatch job ID of every request. Chained requests will have separate entries for the chained request's wmLHE request and GS request with a shared job ID. When the batch jobs finish, `testRequests.py` can be run again to update the CSV file to include the time and size per event. This CSV file can be used with [manageRequests.py](manageRequests.py) to add the time and size per event to McM.

### Creating tests

If you are testing a chained request, you must first [get cookies](#get-cookies) to access McM to get the chained request's component request PrepIDs. No other operations require that.

Create a test of requests with the command

`python testRequests.py -i PrepIDList`

The list of PrepIDs should be formatted as stated [above](#format-of-prepid-lists).

The output CSV file can be specified with the flag `-o file.csv`. The default filename is `test.csv`. The number of events tested will be McM's default. To use N events for all tests, add the flag `-n N`.

### Extracting test results

To extract the time and size per event from the tests, run the command

`python testRequests.py -f file.csv`

on the file created when the tests were submitted.

The script will extract the average time and size of events and store it in the CSV file. If `testRequests.py` is run before all batch jobs finish, it will tell you how many requests still need to have their information filled. The script can be run any number of times to update the remaining requests.

Usage of validateChains.py
--------------------------

To validate multiple chained requests in McM run the command

`python validateChains.py PrepIDList`

where the list of PrepIDs has been formatted as [above](#format-of-prepid-lists).

Usage of checkRequests.py
-------------------------

[checkRequests.py](checkRequests.py) will check the status of requests as well as those chained to them. Format the list of PrepIDs as [above](#format-of-prepid-lists). For example, if you check a wmLHE request that is chained to GS and DR ones, it will display the status of all three (presumably "done" for the first two).

Usage of copyGridpacks.sh
-------------------------

[copyGridpacks.sh](copyGridpacks.sh) will copy gridpacks based on a CSV file to EOS, where they will be automatically copied to cvmfs. The CSV file must contain a column with the header "Local gridpack location". This is the current location of the gridpacks with their full path. The file must also contain a column with the header "Gridpack location". This is the location in cvmfs that you would like the gridpacks to be placed in. The script will change the path of "Gridpack location" from cvmfs to EOS. If a directory does not exist in EOS, the script will make it. (This script has been broken. Automatically creating new directories does not work and script may need to be run as `source copyGridpacks.sh` after setting up a CMSSW environment.)

Usage of copyPrivateLHEs.sh
---------------------------

[copyPrivateLHEs.sh](copyPrivateLHEs.sh) will copy private LHE files to EOS based on a CSV file and `cmsLHEtoEOSManager.py`. It will store the article ID along with the contents of the input CSV file in a new CSV file. You can choose the name of the output CSV file with the flag `-o`. The flag `-a` will append the output to an existing CSV file (make sure that the order of columns is the same as your input file). The flag `-f` will overwrite an existing output file.

The flag `-r` will rename the LHE files before they are stored in EOS to match the "Dataset name" in the CSV file.

Usage of getMcMTestScript.sh
----------------------------

[getMcMTestScript.sh](getMcMTestScript.sh) gets a request's test script from McM and modifies it. Executing the command

`sh getMcMTestScript PrepID`

will save the test script as `test.sh`. Run `sh test.sh` to execute the test locally. The destination file can be modified by the flag `-o` and the number of events can be modified using the flag `-n`.

Usage of getTimeSize.sh
-----------------------

[getTimeSize.sh](getTimeSize.sh) extracts the time per event and size per event from a job report. After running

`cmsRun -e -j log.xml test_cfg.py`

to measure the time and size of a request, you can extract the time per event in seconds and calculate the size per event in kilobytes by running

`sh getTimeSize.sh log.xml`
