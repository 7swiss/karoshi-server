#!/bin/bash
#modify_groups
#Copyright (C) 2007  Paul Sharrad

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
MOD_CODE=`echo ${RANDOM:0:3}`
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/user/modify_groups ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/user/modify_groups

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
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>'$TITLE'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi">
  <link rel="stylesheet" href="/css/'$STYLESHEET'">
<script src="/all/stuHover.js" type="text/javascript"></script>
</head>
<body onLoad="start()">'
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
echo '<form action="/cgi-bin/admin/modify_groups.cgi" method="post">
  <div id="actionbox">
  <b>'$TITLE'</b> 
<a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Modify_Groups"><img class="images" alt="" src="/images/help/info.png"><span>'$HELPMSG1'</span></a>
<br><br>
  <table class="standard" style="text-align: left; left: 232px;" border="0" cellpadding="2" cellspacing="2">
    <tbody>
<tr><td style="width: 180px;">
'$PRIGROUPMSG'</td><td>'
/opt/karoshi/web_controls/group_dropdown_list
echo '</td><td>
<a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Modify_Groups"><img class="images" alt="" src="/images/help/info.png"><span>'$HELPMSG2'</span></a>
</td></tr>
<tr><td>'$OPTIONMSG'</td><td>
<select name="_OPTIONCHOICE_" style="width: 200px;">
<option value="enable">'$ENABLEMSG'</option>
<option value="disable">'$DISABLEMSG'</option>
<option value="deleteaccounts">'$DELETEMSG'</option>
<option value="resetpasswords">'$RESETPASSMSG'</option>
</select></td></tr>
<tr><td style="width: 180px;">
'$EXECPTIONMSG'
</td><td>
<input tabindex= "1" name="_EXCEPTIONLIST_" style="width: 200px;" size="20" type="text">
</td><td>
<a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Modify_Groups"><img class="images" alt="" src="/images/help/info.png"><span>'$EXCEPTIONHELP'</span></a>
</td></tr>
<tr><td>'$CODEMSG'</td><td style="vertical-align: top; text-align: left;"><b>'$MOD_CODE'</b></td></tr>
<tr><td>'$CONFIRMMSG'</td><td style="vertical-align: top; text-align: left;"><input name="_MODCODE_" maxlength="3" size="3" type="text"></td><td>
<a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Modify_Groups"><img class="images" alt="" src="/images/help/info.png"><span>'$HELPMSG3'</span></a>

</td></tr>
    </tbody>
  </table>
<input name="_FORMCODE_" value="'$MOD_CODE'" type="hidden">
  </div>
  <div id="submitbox">
  <input value="'$SUBMITMSG'" type="submit"> <input value="'$RESETMSG'" type="reset">
  </div>
</form>
</body>
</html>
'
exit
