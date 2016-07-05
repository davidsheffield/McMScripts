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
                        "submitted", "done", "absent", "extra"]
            sum_known = requests[i][1] + requests[i][2] + requests[i][3] + requests[i][4] + requests[i][5] + requests[i][6] + requests[i][7]
            total = max(request_set[4], sum_known)
            x_pos = 0.0
            tmp_object_counter = object_counter
            for j in range(7):
                bar_width = 0.0
                if total != 0:
                    if requests[i][j+1] <= request_set[4]:
                        bar_width = float(requests[i][j+1])/float(total)*100.0
                    else:
                        bar_width = float(request_set[4])/float(total)*100.0
                    if bar_width < 0.0:
                        bar_width = 0.0
                fout.write("""\
                    <rect x="{0}" y="18" width="{1}" height="30" class="{2}" onmouseover="show(evt, 'object{3}')" onmouseout="hide(evt, 'object{3}')" />
""".format(x_pos, bar_width, statuses[j], tmp_object_counter))
                x_pos += bar_width
                tmp_object_counter += 1
            unkown_reason = "absent"
            if total > request_set[4]:
                unkown_reason = "extra"
                # if x_pos >= 95.0:
                #     x_pos = 95.0
            fout.write("""\
                    <rect x="{0}" y="18" width="{1}" height="30" class="{2}" onmouseover="show(evt, 'object{3}')" onmouseout="hide(evt, 'object{3}')" />
""".format(x_pos, max(100.0 - x_pos, 0.0), unkown_reason, tmp_object_counter))
            fout.write("""\
                </g>
            </a>
""")
            for j in range(7):
                fout.write("""\
            <g id="object{0}" display="none" class="tooltip">
                <path d="M0 18 V7 Q0 0 7 0 H93 Q100 0 100 7 V18" class="{1}" />
                <text x="10" y="14">{2} {1}</text>
            </g>
""".format(object_counter, statuses[j], requests[i][j+1]))
                object_counter += 1
            fout.write("""\
            <g id="object{0}" display="none" class="tooltip">
                <path d="M0 18 V7 Q0 0 7 0 H93 Q100 0 100 7 V18" class="{1}" />
                <text x="10" y="14">{2} {1}</text>
            </g>
""".format(object_counter, unkown_reason, max(total - sum_known, sum_known - request_set[4])))
            object_counter += 1
            fout.write("""\
        </svg>
""")
            fout.write("    </td>\n")
        elif page == 1:
            fout.write("    <td class=\"{0}\">\n".format(campaign_classes[i + class_offset]))
            fout.write("""\
        <svg width="100" height="48" class="status">
            <a xlink:href="https://cms-pdmv.cern.ch/mcm/requests?tags={0}&member_of_campaign={1}&page=-1" target="_blank">
                <g class="bar">
""".format(request_set[2], requests[i][0]))
            statuses = ["new", "validating", "validated", "defined", "approved",
                        "submitted", "done", "absent", "extra"]
            sum_known = requests[i][1] + requests[i][2] + requests[i][3] + requests[i][4] + requests[i][5] + requests[i][6] + requests[i][7]
            total = max(request_set[4], sum_known)
            combined_statuses = ["preparation", "ready to run", "running",
                                 "done", "absent", "extra"]
            combined_classes = [statuses[0], statuses[4], statuses[5], statuses[6]]
            combined_requests = [requests[i][1] + requests[i][2] + requests[i][3],
                                 requests[i][4] + requests[i][5], requests[i][6],
                                 requests[i][7]]
            x_pos = 0.0
            tmp_object_counter = object_counter
            for j in range(4):
                bar_width = 0.0
                if total != 0:
                    bar_width = float(combined_requests[j])/float(total)*100.0
                    if bar_width < 0.0:
                        bar_width = 0.0
                fout.write("""\
                    <rect x="{0}" y="18" width="{1}" height="30" class="{2}" onmouseover="show(evt, 'object{3}')" onmouseout="hide(evt, 'object{3}')" />
""".format(x_pos, bar_width, combined_classes[j], tmp_object_counter))
                x_pos += bar_width
                tmp_object_counter += 1
            unkown_reason = "absent"
            if total > request_set[4]:
                unkown_reason = "extra"
            fout.write("""\
                    <rect x="{0}" y="18" width="{1}" height="30" class="{2}" onmouseover="show(evt, 'object{3}')" onmouseout="hide(evt, 'object{3}')" />
""".format(x_pos, max(100.0 - x_pos, 0.0), unkown_reason, tmp_object_counter))
            fout.write("""\
                </g>
            </a>
""")
            for j in range(4):
                fout.write("""\
            <g id="object{0}" display="none" class="tooltip">
                <path d="M0 18 V7 Q0 0 7 0 H93 Q100 0 100 7 V18" class="{1}" />
                <text x="10" y="14">{2} {3}</text>
            </g>
""".format(object_counter, combined_classes[j], combined_requests[j],
           combined_statuses[j]))
                object_counter += 1
            fout.write("""\
            <g id="object{0}" display="none" class="tooltip">
                <path d="M0 18 V7 Q0 0 7 0 H93 Q100 0 100 7 V18" class="{1}" />
                <text x="10" y="14">{2} {1}</text>
            </g>
""".format(object_counter, unkown_reason, total - sum_known))
            object_counter += 1
            fout.write("""\
        </svg>
""")
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
    <td class="requests">{6}</td>
""".format(request_set[1], request_set[2], instance[3], instance[2],
           instance[1], display_number(request_set[3]), request_set[4]))
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
                fout.write("    <td class=\"spreadsheet\"><a href=\"{0}\" target=\"_blank\" title=\"spreadsheet\"><span class=\"spreadsheet_icon\">&nbsp;</div></a></td>\n".format(
                        request_set[6]))
            if request_set[5] == "":
                fout.write("    <td class=\"notes\">&nbsp;</td>\n")
            else:
                fout.write("    <td class=\"notes\"><span class=\"ref\"><span class=\"note_icon\">&nbsp;</span><span class=\"note_content\">{0}</span></span></td>\n".format(request_set[5]))
        elif page == 1:
            if request_set[6] == "":
                fout.write("    <td class=\"spreadsheet empty\">&nbsp;</td>\n")
            else:
                fout.write("    <td class=\"spreadsheet\"><a href=\"{0}\" target=\"_blank\" title=\"spreadsheet\"><span class=\"spreadsheet_icon\">&nbsp;</div></a></td>\n".format(
                        request_set[6]))
            if request_set[5] == "":
                fout.write("    <td class=\"notes\">&nbsp;</td>\n")
            else:
                fout.write("    <td class=\"notes\"><span class=\"ref\"><span class=\"note_icon\">&nbsp;</span><span class=\"note_content\">{0}</span></span></td>\n".format(request_set[5]))
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
    fout.write("""\
<div class="toc">
    <h2>Campaigns:</h2>
    <ul>
""")
    for super_campaign in super_campaigns:
        fout.write("""\
        <li><a href="#{0}">{1}</a></li>
""".format(super_campaign[1].replace(" ", "-"), super_campaign[1]))
    fout.write("""\
    </ul>
</div>

""")

    for super_campaign in super_campaigns:
        fout.write("""\
<h2 class="campaign" id="{0}">{1}</h2>
<table>
<thead>
<tr class="table_header">
""".format(super_campaign[1].replace(" ", "-"), super_campaign[1]))
        if page == 0:
            fout.write("""\
    <th class="process">Process</th>
    <th class="tag">Tag</th>
    <th class="requester">Requester</th>
    <th class="contact">Contact</th>
    <th class="events">Events</th>
    <th class="requests">Requests</th>
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
        fout.write("</tr>\n</thead>\n<tbody>\n")

        writeRequestSets(page, fout, c, super_campaign)

        fout.write("</tbody>\n</table>\n")

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

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
    <script>
      jQuery.noConflict();
      jQuery(function() {
        jQuery(".note_content").hide();
        jQuery(".note_icon").click(function(event) {
          jQuery(this.nextSibling).toggle();
          event.stopPropagation();
        });
      });
    </script>
</head>

<body>

<div class="wrapper">
<h1>Exotica MC</h1>

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
<div class="update-time">Updated {0}</p>
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

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
    <script>
      jQuery.noConflict();
      jQuery(function() {
        jQuery(".note_content").hide();
        jQuery(".note_icon").click(function(event) {
          jQuery(this.nextSibling).toggle();
          //jQuery(this).toggle(jQuery(this).css("background", "url(sprites.png) -48px -6px"), jQuery(this).css("background", "url(sprites.png) -6px -89px"));
          event.stopPropagation();
        });
        //jQuery("body").click(function(event) {
        //  jQuery(".note_content").hide();
        //});
      });
    </script>
</head>

<body>

<div class="wrapper">
<h1>Exotica MC</h1>

<p><a href="analyzer.html">Go to analyzer page</a></p>

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
<div class="update-time">Updated {0}</p>
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
