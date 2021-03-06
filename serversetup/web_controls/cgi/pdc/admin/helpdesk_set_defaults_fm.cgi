#!/bin/bash
#Copyright (C) 2012  Paul Sharrad

#This file is part of Karoshi Server.
#
#Karoshi Server is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Karoshi Server is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Karoshi Server.  If not, see <http://www.gnu.org/licenses/>.

#
#The Karoshi Team can be contacted at: 
#mpsharrad@karoshi.org.uk
#jharris@karoshi.org.uk
#aball@karoshi.org.uk
#
#Website: http://www.karoshi.org.uk
############################
#Language
############################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/user/helpdesk ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/user/helpdesk
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all
#Check if timout should be disabled
if [ `echo $REMOTE_ADDR | grep -c $NOTIMEOUT` = 1 ]
then
TIMEOUT=86400
fi
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>'$TITLE5'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi">
<link rel="stylesheet" href="/css/'$STYLESHEET'">
<script src="/all/stuHover.js" type="text/javascript"></script>
</head>
<body onLoad="start()">'

#Get defaults

#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
echo '<form action="/cgi-bin/admin/helpdesk_set_defaults.cgi" method="post"><div id="actionbox"><b>'$TITLE5'</b><br><br>
  <table class="standard" style="text-align: left;" border="0" cellpadding="2" cellspacing="2">
<tbody>
<tr><td style="width: 180px;">'$DEFAULTNAMEMSG'</td><td>
<select tabindex= "1" style="width: 200px;" name="_DEFAULTNAME_">'

if [ -f /opt/karoshi/helpdesk/defaultassign ]
then
ASSIGNED=`sed -n 1,1p /opt/karoshi/helpdesk/defaultassign`
echo '<option value="'$ASSIGNED'">'$ASSIGNED'</option>
'
else
ASSIGNED=no
fi
echo '<option value="NODEFAULTNAME">'$NODEFAULTMSG'</option>'
for ADMINUSER in `cat /opt/karoshi/web_controls/web_access_admin | cut -d: -f1`
do
[ $ADMINUSER != $ASSIGNED ] && echo '<option value="'$ADMINUSER'">'$ADMINUSER'</option>'
done
for TECHUSER in `cat /opt/karoshi/web_controls/web_access_tech | cut -d: -f1`
do
[ $TECHUSER != $ASSIGNED ] && echo '<option value="'$TECHUSER'">'$TECHUSER'</option>'
done
echo '</td><td><a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$HELPMSG5'</span></a></td></tr>
<tr><td>'$DEFAULTPRIORITYMSG'</td><td><select tabindex= "2" style="width: 200px;" name="_DEFAULTPRIORITY_">'

if [ -f /opt/karoshi/helpdesk/defaultpriority ]
then
PRIORITY=`sed -n 1,1p /opt/karoshi/helpdesk/defaultpriority`
echo '<option value="'$PRIORITY'">'$PRIORITY'</option>
'
else
PRIORITY=no
fi
echo '<option value="NODEFAULTPRIORITY">'$NODEFAULTMSG'</option>'
[ $PRIORITY != $PRIORITY1 ] && echo '<option value="'$PRIORITY1'">'$PRIORITY1'</option>'
[ $PRIORITY != $PRIORITY2 ] && echo '<option value="'$PRIORITY2'">'$PRIORITY2'</option>'
[ $PRIORITY != $PRIORITY3 ] && echo '<option value="'$PRIORITY3'">'$PRIORITY3'</option>'
[ $PRIORITY != $PRIORITY1 ] && echo '<option value="'$PRIORITY4'">'$PRIORITY4'</option>'

echo '</td><td><a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$HELPMSG6'</span></a></td></tr></tbody></table><br>
</div>
<div id="submitbox">
<input value="'$SUBMITMSG'" type="submit"> <input value="'$RESETMSG'" type="reset">
</div>
</form>
</body>
</html>
'
exit

