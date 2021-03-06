#!/bin/bash
#Copyright (C) 2011  Paul Sharrad

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

#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser

############################
#Language
############################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/printer/printer_accounting ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/printer/printer_accounting
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
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$TITLE2'</title><META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE"><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi"><link rel="stylesheet" href="/css/'$STYLESHEET'"><script src="/all/stuHover.js" type="text/javascript"></script><meta name="viewport" content="width=device-width, initial-scale=1"> <!--480-->'
if [ $MOBILE = yes ]
then
echo '<link rel="stylesheet" type="text/css" href="/all/mobile_menu/sdmenu.css">
	<script type="text/javascript" src="/all/mobile_menu/sdmenu.js">
		/***********************************************
		* Slashdot Menu script- By DimX
		* Submitted to Dynamic Drive DHTML code library: http://www.dynamicdrive.com
		* Visit Dynamic Drive at http://www.dynamicdrive.com/ for full source code
		***********************************************/
	</script>
	<script type="text/javascript">
	// <![CDATA[
	var myMenu;
	window.onload = function() {
		myMenu = new SDMenu("my_menu");
		myMenu.init();
	};
	// ]]>
	</script>'
fi
echo '</head><body onLoad="start()">'

#Generate navigation bar
if [ $MOBILE = no ]
then
DIV_ID=actionbox
TABLECLASS=standard
WIDTH=180
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
else
DIV_ID=actionbox2
TABLECLASS=mobilestandard
WIDTH=110
fi
echo '<form name="myform" action="/cgi-bin/admin/printer_accounting_edit_limits_fm.cgi" method="post">'

[ $MOBILE = no ] && echo '<div id="'$DIV_ID'">'

#Show back button for mobiles
if [ $MOBILE = yes ]
then
echo '<div style="float: center" id="my_menu" class="sdmenu">
	<div class="expanded">
	<span>'$TITLE2'</span>
<a href="/cgi-bin/admin/mobile_menu.cgi">'$PRINTMENUMSG'</a>
</div></div><div id="mobileactionbox">
'
else
echo '<b>'$TITLE2'</b> <a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Printer_Accounting#Group_Limits"><img class="images" alt="" src="/images/help/info.png"><span>'$HELPMSG3'<br><br>'$HELPMSG4'</span></a>
<br><br>'
fi

echo '<table class="'$TABLECLASS'" style="text-align: left;" border="0" cellpadding="2" cellspacing="2"><tbody>
<tr><td style="width: '$WIDTH'px;"><b>'$PRIMARYGROUPMSG'</b></td><td><b>'$LIMITMSG'</b></td><td><a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Printer_Accounting#Group_Limits"><img class="images" alt="" src="/images/help/info.png"><span>'$HELPMSG5'</span></a></td></tr>'

ICON1=/images/submenus/printer/edit_printer_limits.png
for NAMES in /opt/karoshi/server_network/printer_accounting/quotas/*_group_quota
do
NAME1=`basename $NAMES`
NAME2=`basename $NAMES | cut -d_ -f1`
LIMIT=`sed -n 1,1p /opt/karoshi/server_network/printer_accounting/quotas/$NAME1`
echo '<tr><td>'$NAME2'</td><td>'$LIMIT'</td><td>
<input src="'$ICON1'" name="_NAME_'$NAME1'_LIMIT_'$LIMIT'_TYPE_group_" type="image" value="'$NAME2' - '$EDITLIMITMSG'">
</td></tr>'
done

echo '</tbody></table><br></div></form></body></html>'
exit

