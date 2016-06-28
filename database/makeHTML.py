#!/usr/bin/env python

################################
#
# check.py
#
#  Script to check status of requests and save in database
#
#  author: David G. Sheffield (Rutgers)
#
################################

import sqlite3
import argparse
import sys
import math
import shutil
sys.path.append('../')
import mcmscripts_config

# Global variables
object_counter = 0


def display_number(n):
    if n == 0:
        return "0"
    else:
        prefix = ['', 'k', 'M']
        n = float(n)
        prefix_id = max(0, min(2, int(math.floor(math.log10(abs(n))/3.0))))
        return "{0:.5g}{1}".format(n/10**(3*prefix_id), prefix[prefix_id]);


def writeRequests(page, fout, c, super_campaign, request_set, instance):
    campaign_classes = ["lhe", "gs", "dr", "miniaod"]
    global object_counter

    c.execute("""\
SELECT Campaigns.Name,
       New,
       Validating,
       Validated,
       Defined,
       Approved,
       Submitted,
       Done
FROM Requests
INNER JOIN Instance_Requests USING(RequestsID)
INNER JOIN Campaigns USING(CampaignID)
WHERE InstanceID = {0}
ORDER BY Level""".format(instance[0]))
    requests = c.fetchall()
    class_offset = 0
    if len(requests) < 4:
        fout.write("    <td class=\"lhe\">&nbsp;</td>\n")
        class_offset = 1
    for i in range(len(requests)):
        if page == 0:
            fout.write("    <td class=\"{0}\">\n".format(campaign_classes[i + class_offset]))
            fout.write("""\
        <svg width="100" height="48" class="status">
            <a xlink:href="https://cms-pdmv.cern.ch/mcm/requests?tags={0}&member_of_campaign={1}&page=-1" target="_blank">
                <g class="bar">
""".format(request_set[2], requests[i][0]))
            statuses = ["new", "validating", "validated", "defined", "approved",
                        "submitted", "done", "unkown"]
            x_pos = 0.0
            tmp_object_counter = object_counter
            for j in range(7):
                bar_width = 0.0
                if request_set[4] != 0:
                    bar_width = float(requests[i][j+1])/float(request_set[4])*100.0
                fout.write("""\
                    <rect x="{0}" y="18" width="{1}" height="30" class="{2}" onmouseover="show(evt, 'object{3}')" onmouseout="hide(evt, 'object{3}')" />
""".format(x_pos, bar_width, statuses[j], tmp_object_counter))
                x_pos += bar_width
                tmp_object_counter += 1
            fout.write("""\
                    <rect x="{0}" y="18" width="{1}" height="30" class="unknown" onmouseover="show(evt, 'object{2}')" onmouseout="hide(evt, 'object{2}')" />
""".format(x_pos, 100.0 - x_pos, tmp_object_counter))
            fout.write("""\
                </g>
            </a>
""")
            for j in range(7):
                fout.write("""\
            <g id="object{0}" display="none" class="tooltip">
                <!--<rect x="0" y="0" width="100.0" height="18" class="{1}" />-->
                <path d="M0 18 V10 Q0 0 10 0 H90 Q100 0 100 10 V18" class="{1}" />
                <text x="10" y="15">{2} {1}</text>
            </g>
""".format(object_counter, statuses[j], requests[i][j+1]))
                object_counter += 1
            fout.write("""\
            <g id="object{0}" display="none" class="tooltip">
                <!--<rect x="0" y="0" width="100.0" height="18" class="unknown" />-->
                <path d="M0 18 V10 Q0 0 10 0 H90 Q100 0 100 10 V18" class="unknown" />
                <text x="10" y="15">{1} unkown</text>
            </g>
""".format(object_counter, 0))
            object_counter += 1
            fout.write("""\
        </svg>
""")
            fout.write("    </td>\n")
        elif page == 1:
            # fout.write("    <td class=\"{0}\"><a href=\"https://cms-pdmv.cern.ch/mcm/requests?tags={1}&member_of_campaign={2}&page=-1\" class=\"status\">{3}/{4}</a></td>\n".format(
            #         campaign_classes[i + class_offset], request_set[2],
            #         requests[i][0], requests[i][7], request_set[4]))
            fout.write("    <td class=\"{0}\">\n".format(campaign_classes[i + class_offset]))
            fout.write("        <a href=\"https://cms-pdmv.cern.ch/mcm/requests?tags={0}&member_of_campaign={1}&page=-1&shown=274877909023\" class=\"status\" target=\"_blank\"><img src=\"http://chart.apis.google.com/chart?chbh=a,0&amp;chs=100x30&amp;cht=bhs:nda&amp;chco=ccccff,cc99ff,6ba6e8,52fbc4,ffeba4,ffc570,66aa66,ff4500&amp;chds=0,{6},0,{6},0,{6},0,{6},0,{6},0,{6},0,{6},0,{6}&amp;chd=t:{2}|0|0|0|{3}|{4}|{5}|0\" alt=\"{2} {3} {4} {5} / {6}\" title=\"{1} {2} preparation, {3} approved, {4} running, {5} done / {6}\"></a>\n".format(
                    request_set[2], requests[i][0],
                    requests[i][1] + requests[i][2] + requests[i][3] + requests[i][4],
                    requests[i][5], requests[i][6], requests[i][7],
                    request_set[4]))
            fout.write("    </td>\n")
    return


def writeInstances(page, fout, c, super_campaign, request_set):
    c.execute("""\
SELECT InstanceID,
       DisplayName,
       Requesters.Name,
       Requesters.Email,
       CampaignChains.Name
FROM Instances
INNER JOIN Contacts USING(ContactID)
INNER JOIN Requesters USING(RequesterID)
INNER JOIN CampaignChains USING(CampaignChainID)
WHERE SetID = {0}
  AND SuperCampaignID = {1};""".format(request_set[0], super_campaign[0]))
    instances = c.fetchall()
    for instance in instances:
        fout.write("<tr>\n")
        if page == 0:
            fout.write("""\
    <td class="process">{0}</td>
    <td class="tag">{1}</td>
    <td class="requester"><a href="mailto:{2}">{3}</a></td>
    <td class="contact">{4}</td>
    <td class="events">{5}</td>
""".format(request_set[1], request_set[2], instance[3], instance[2],
           instance[1], display_number(request_set[3])))
        elif page == 1:
            fout.write("""\
    <td class="process">{0}</td>
    <td class="requester"><a href="mailto:{1}">{2}</a></td>
""".format(request_set[1], instance[3], instance[2]))
        writeRequests(page, fout, c, super_campaign, request_set, instance)
        if page == 0:
            if request_set[6] == "":
                fout.write("    <td class=\"spreadsheet empty\">&nbsp;</td>\n")
            else:
                fout.write("    <td class=\"spreadsheet\"><a href=\"{0}\" target=\"_blank\" title=\"spreadsheet\"><div class=\"spreadsheet_icon\">&nbsp;</div></a></td>\n".format(
                        request_set[6]))
            if request_set[5] == "":
                fout.write("    <td class=\"notes\">&nbsp;</td>\n")
            else:
                fout.write("    <td class=\"notes\">{0}</td>\n".format(request_set[5]))
        elif page == 1:
            if request_set[6] == "":
                fout.write("    <td class=\"spreadsheet empty\">&nbsp;</td>\n")
            else:
                fout.write("    <td class=\"spreadsheet\"><a href=\"{0}\" target=\"_blank\" title=\"spreadsheet\"><div class=\"spreadsheet_icon\">&nbsp;</div></a></td>\n".format(
                        request_set[6]))
            if request_set[5] == "":
                fout.write("    <td class=\"notes\">&nbsp;</td>\n")
            else:
                fout.write("    <td class=\"notes\">{0}</td>\n".format(request_set[5]))
        fout.write("</tr>\n")
    return


def writeRequestSets(page, fout, c, super_campaign):
    c.execute("""\
SELECT DISTINCT SetID,
                Process,
                Tag,
                Events,
                RequestMultiplicity,
                Notes,
                Spreadsheet
FROM RequestSets
INNER JOIN Instances USING(SetID)
INNER JOIN CampaignChains USING(CampaignChainID)
WHERE SuperCampaignID = {0};""".format(super_campaign[0]))
    request_sets = c.fetchall()
    for request_set in request_sets:
        writeInstances(page, fout, c, super_campaign, request_set)
    return


def writeSuperCampaigns(page, fout, c):
    global object_counter
    object_counter = 0
    c.execute("""\
SELECT SuperCampaignID,
       Name
FROM SuperCampaigns
ORDER BY Active;""")
    super_campaigns = c.fetchall()
    for super_campaign in super_campaigns:
        fout.write("""\
<h2 class="campaign">{0}</h2>
<table>
<tr class="table_header">
""".format(super_campaign[1]))
        if page == 0:
            fout.write("""\
    <th class="process">Process</th>
    <th class="tag">Tag</th>
    <th class="requester">Requester</th>
    <th class="contact">Contact</th>
    <th class="events">Events</th>
    <th class="lhe">LHE</th>
    <th class="gs">GS</th>
    <th class="dr">DR</th>
    <th class="miniaod">MiniAOD</th>
    <th class="spreadsheet">Spreadsheet</th>
    <th class="notes">Notes</th>
""")
        elif page == 1:
            fout.write("""\
    <th class="process">Process</th>
    <th class="requester">Requester</th>
    <th class="lhe">LHE</th>
    <th class="gs">GS</th>
    <th class="dr">DR</th>
    <th class="miniaod">MiniAOD</th>
    <th class="spreadsheet">Spreadsheet</th>
    <th class="notes">Notes</th>
""")
        fout.write("</tr>\n")

        writeRequestSets(page, fout, c, super_campaign)

        fout.write("</table>\n")

    return


def makeAnalyzerHTML():
    fout = open('{0}analyzer.html'.format(mcmscripts_config.html_location), 'w')
    campaign_classes = ["lhe", "gs", "dr", "miniaod", "miniaodv2"]

    fout.write("""\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html>
<head>
    <title>Exotica MC Status for Analyzers</title>

    <link rel="stylesheet" type="text/css" href="global.css">
    <link rel="icon" href="favicon.ico" type="image/x-icon">

    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
</head>

<body>

<div class="wrapper">
<h1>Exotica MC</h1>

<table><tr>
    <td class="gs" style="background-color:#ccccff">Preparing requests</td>
    <td class="gs" style="background-color:#ffeba4">Approved to run</td>
    <td class="gs" style="background-color:#ffc570">Running</td>
    <td class="gs" style="background-color:#66aa66">Done</td>
</tr></table>

""")

    conn = sqlite3.connect(mcmscripts_config.database_location)

    c = conn.cursor()
    writeSuperCampaigns(1, fout, c)

    c.execute("""\
SELECT Value
FROM Settings
WHERE SettingID = 1""")
    check_time = c.fetchone()
    fout.write("""\
</table>
<p class="update-time">Updated {0}</p>
</div>

</body>
</html>
""".format(check_time[0]))
    fout.close()

    print "Generated analyzer page"

    return


def makeContactHTML():
    fout = open('{0}contact.html'.format(mcmscripts_config.html_location), 'w')
    campaign_classes = ["lhe", "gs", "dr", "miniaod", "miniaodv2"]

    fout.write("""\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html>
<head>
    <title>Exotica MC Status for Contacts</title>

    <link rel="stylesheet" type="text/css" href="global.css">
    <link rel="icon" href="favicon.ico" type="image/x-icon">

    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">

    <svg width="0" height="0">
        <script>
            <![CDATA[
            function show(evt, node) {
                var svgdoc = evt.target.ownerDocument;
                var obj = svgdoc.getElementById(node);
                obj.setAttribute("display", "inline");
            }

            function hide(evt, node) {
                var svgdoc = evt.target.ownerDocument;
                var obj = svgdoc.getElementById(node);
                obj.setAttribute("display" , "none");
            }
            ]]>
        </script>
    </svg>
</head>

<body>

<div class="wrapper">
<h1>Exotica MC</h1>

<table><tr>
    <td class="gs" style="background-color:#ccccff">New</td>
    <td class="gs" style="background-color:#cc99ff">Validating</td>
    <td class="gs" style="background-color:#6ba6e8">Validated</td>
    <td class="gs" style="background-color:#52fbc4">Defined</td>
    <td class="gs" style="background-color:#ffeba4">Approved</td>
    <td class="gs" style="background-color:#ffc570">Submitted</td>
    <td class="gs" style="background-color:#66aa66">Done</td>
</tr></table>

""")

    # <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    # <script type="text/javascript">
    #     google.charts.load('current', {packages: ['corechart', 'bar']});
    # </script>

    conn = sqlite3.connect(mcmscripts_config.database_location)

    c = conn.cursor()
    writeSuperCampaigns(0, fout, c)

    c.execute("""\
SELECT Value
FROM Settings
WHERE SettingID = 1""")
    check_time = c.fetchone()
    fout.write("""\
</table>
<p class="update-time">Updated {0}</p>
</div>

</body>
</html>
""".format(check_time[0]))
    fout.close()

    print "Generated contact page"

    return


def syncAuxiliaryFiles():
    shutil.copyfile("global.css", "{0}global.css".format(mcmscripts_config.html_location))
    shutil.copyfile("favicon.ico", "{0}favicon.ico".format(mcmscripts_config.html_location))
    shutil.copyfile("sprites.png", "{0}sprites.png".format(mcmscripts_config.html_location))

    print "Copied auxiliary files"

    return


def main():
    makeAnalyzerHTML()
    makeContactHTML()
    syncAuxiliaryFiles()

    return


if __name__ == '__main__':
    main()
