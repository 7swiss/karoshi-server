#!/bin/bash
#Copyright (C) 2007 Paul Sharrad

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
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/internet/dg_room_controls ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/internet/dg_room_controls
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
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$TITLE'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi"><link rel="stylesheet" href="/css/'$STYLESHEET'"><script src="/all/stuHover.js" type="text/javascript"></script><meta name="viewport" content="width=device-width, initial-scale=1"> <!--480-->'

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

echo '</head><body>'
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:%\+-'`
#########################
#Assign data to variables
#########################
END_POINT=6

#Assign _LOCATION_
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = LOCATIONcheck ]
then
let COUNTER=$COUNTER+1
LOCATION=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo '                window.location = "/cgi-bin/admin/dg_room_controls_fm.cgi";'
echo '</script>'
echo "</body></html>"
exit
}
#########################
#Check https access
#########################
if [ https_$HTTPS != https_on ]
then
export MESSAGE=$ERRORMSG7
show_status
fi

#########################
#Check data
#########################

#Check to see that LOCATION is not blank
if [ $LOCATION'null' = null ]
then
MESSAGE=$ERRORMSG1
show_status
fi


#Generate navigation bar
if [ $MOBILE = no ]
then
DIV_ID=actionbox
TABLECLASS=standard
WIDTH=60
WIDTH2=120
TABLETITLE="$TITLE - $LOCATION"
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
echo '<div id="'$DIV_ID'">'
else
DIV_ID=menubox
TABLECLASS=mobilestandard
WIDTH=50
WIDTH2=80
TABLETITLE="$LOCATION"

echo '<div style="float: center" id="my_menu" class="sdmenu">
	<div class="expanded">
	<span>'$TITLE'</span>
<a href="/cgi-bin/admin/mobile_menu.cgi">'$INTERNETMENUMSG'</a>
</div></div><div id="mobileactionbox">
'
fi

ICON1=/images/submenus/internet/client_allowed.png
ICON2=/images/submenus/internet/client_denied.png
ICON3=/images/assets/location.png

echo '<table class="'$TABLECLASS'" style="text-align: left;" border="0" cellpadding="2" cellspacing="2">
<tr><td style="vertical-align: top;"><b>'$TABLETITLE'</b></td>
<td style="vertical-align: top;"><form action="/cgi-bin/admin/dg_room_controls_fm.cgi" method="post"><a class="info" href="javascript:void(0)"><input name="" type="image" class="images" src="'$ICON3'" value=""><span>'$CHOOSELOCATIONMSG'</span></a></form></td>
<td style="vertical-align: top;"><form action="/cgi-bin/admin/dg_room_controls2.cgi" method="post"><a class="info" href="javascript:void(0)"><input name="_LOCATION_'$LOCATION'_ACTION_allowall_ASSET_na_" type="image" class="images" src="'$ICON1'" value=""><span>'$ALLOWALLMSG'</span></a></form></td>
<td style="vertical-align: top;"><form action="/cgi-bin/admin/dg_room_controls2.cgi" method="post"><a class="info" href="javascript:void(0)"><input name="_LOCATION_'$LOCATION'_ACTION_denyall_ASSET_na_" type="image" class="images" src="'$ICON2'" value=""><span>'$DENYALLMSG'</span></a></form></td>
<td valign=top><a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Room_Controls"><img class="images" alt="" src="/images/help/info.png"><span>'$HELPMSG2'</span></a></td>'

#Show reset times
if [ -d /opt/karoshi/server_network/internet_room_controls_reset ]
then
if [ `ls -1 /opt/karoshi/server_network/internet_room_controls_reset | wc -l` -gt 0 ]
then
echo '<td style="vertical-align: top;"><a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Room_Controls"><img class="images" alt="" src="/images/submenus/internet/reset_room_controls_add.png"><span>'$HELPMSG4':<br>'
ls /opt/karoshi/server_network/internet_room_controls_reset | sed 's/$/<br>/g'
echo '</span></a></td>'
fi
fi

echo '</tr></table><br>'

if [ -d /opt/karoshi/asset_register/locations/$LOCATION/ ]
then
if [ `ls -1 /opt/karoshi/asset_register/locations/$LOCATION/ | wc -l` -gt 0 ]
then
echo '<table class="'$TABLECLASS'" style="text-align: left;" border="0" cellpadding="2" cellspacing="2">
<tbody><tr><td style="width: '$WIDTH'px;"><b>'$ASSETMSG'</b></td><td style="width: '$WIDTH2'px;"><b>'$MACADDRESSMSG'</b></td><td style="width: '$WIDTH2'px;"><b>'$TCPIPMSG'</b></td><td><b>Status</b></td></tr>'

for ASSETS in "/opt/karoshi/asset_register/locations/$LOCATION/"*
do
ASSET=`basename $ASSETS`
source /opt/karoshi/asset_register/locations/$LOCATION/$ASSET
#Only show certain asset types
if [ $ASSETTYPE = 1 ] || [ $ASSETTYPE = 3 ] || [ $ASSETTYPE = 5 ] || [ $ASSETTYPE = 7 ] || [ $ASSETTYPE = 9 ]
then
ICON=$ICON1
CONTROLMSG=$DENYMSG
ACTION=deny
if [ -f /opt/karoshi/server_network/internet_room_controls/$LOCATION/$ASSET ]
then
ICON=$ICON2
CONTROLMSG=$ALLOWMSG
ACTION=allow
fi
echo '<tr><td style="vertical-align: top;">'$ASSET'</td><td style="vertical-align: top;">'$MAC1'</td><td style="vertical-align: top;">'$TCPIP1'</td><td><form action="/cgi-bin/admin/dg_room_controls2.cgi" method="post"><a class="info" href="javascript:void(0)"><input name="_ACTION_'$ACTION'_LOCATION_'$LOCATION'_ASSET_'$ASSET'_" type="image" class="images" src="'$ICON'" value=""><span>'$CONTROLMSG' '$ASSET'</span></a></form></td></tr>'
fi
done
fi
fi

echo '</tbody></table>'
echo "</div>"
echo "</body></html>"
exit
