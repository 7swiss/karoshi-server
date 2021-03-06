#!/bin/bash
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
########################
#Required input variables
########################
# _LOCKOUTDURATION_
# _LOCKOUTTHRESHOLD_
# _LOCKOUTOBS_
##########################
#Language
##########################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/user/default_user_settings ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/user/default_user_settings
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all
##########################
#Show page
##########################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$TITLE'</title><meta http-equiv="REFRESH" content="0; URL='$HTTP_REFERER'"><link rel="stylesheet" href="/css/'$STYLESHEET'"></head><body>'
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`
#########################
#Assign data to variables
#########################
END_POINT=14
#Assign LOCKOUTDURATION
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = LOCKOUTDURATIONcheck ]
then
let COUNTER=$COUNTER+1
LOCKOUTDURATION=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done
#Assign LOCKOUTTHRESHOLD
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = LOCKOUTTHRESHOLDcheck ]
then
let COUNTER=$COUNTER+1
LOCKOUTTHRESHOLD=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done
#Assign LOCKOUTOBS
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = LOCKOUTOBScheck ]
then
let COUNTER=$COUNTER+1
LOCKOUTOBS=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

#Assign SHADOWMAX
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = SHADOWMAXcheck ]
then
let COUNTER=$COUNTER+1
SHADOWMAX=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

#Assign USERNAMESTYLE
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = USERNAMESTYLEcheck ]
then
let COUNTER=$COUNTER+1
USERNAMESTYLE=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

#Make sure that only numbers are entered
LOCKOUTDURATION=`echo $LOCKOUTDURATION | tr -cd '0-9\n'`
LOCKOUTTHRESHOLD=`echo $LOCKOUTTHRESHOLD | tr -cd '0-9\n'`
LOCKOUTOBS=`echo $LOCKOUTOBS | tr -cd '0-9\n'`
SHADOWMAX=`echo $SHADOWMAX | tr -cd '0-9\n'`

#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
echo '<div id="actionbox"><b>'$TITLE'</b><br><br>'

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo '</script>'
echo "</div></body></html>"
exit
}
#########################
#Check https access
#########################
if [ https_$HTTPS != https_on ]
then
export MESSAGE=$HTTPS_ERROR
show_status
fi
#########################
#Check user accessing this script
#########################
if [ ! -f /opt/karoshi/web_controls/web_access_admin ] || [ $REMOTE_USER'null' = null ]
then
MESSAGE=$ACCESS_ERROR1
show_status
fi

if [ `grep -c ^$REMOTE_USER: /opt/karoshi/web_controls/web_access_admin` != 1 ]
then
MESSAGE=$ACCESS_ERROR1
show_status
fi
#########################
#Check data
#########################
#Check to see that LOCKOUTDURATION is not blank
if [ $LOCKOUTDURATION'null' = null ]
then
MESSAGE=$ERRORMSG1
show_status
fi
#Check to see that LOCKOUTTHRESHOLD is not blank
if [ $LOCKOUTTHRESHOLD'null' = null ]
then
MESSAGE=$ERRORMSG2
show_status
fi
#Check to see that LOCKOUTOBS is not blank
if [ $LOCKOUTOBS'null' = null ]
then
MESSAGE=$ERRORMSG3
show_status
fi

#Check to see that SHADOWMAX is not blank
if [ $SHADOWMAX'null' = null ]
then
MESSAGE=$ERRORMSG4
show_status
fi

#Check to see that USERNAMESTYLE is not blank
if [ $USERNAMESTYLE'null' = null ]
then
MESSAGE=$ERRORMSG5
show_status
fi

MD5SUM=`md5sum /var/www/cgi-bin_karoshi/admin/default_user_settings.cgi | cut -d' ' -f1`
#Modify settings
echo "$REMOTE_USER:$REMOTE_ADDR:$MD5SUM:SETDATA:$LOCKOUTDURATION:$LOCKOUTTHRESHOLD:$LOCKOUTOBS:$SHADOWMAX:$USERNAMESTYLE:" | sudo -H /opt/karoshi/web_controls/exec/default_user_settings
EXEC_STATUS=`echo $?`
if [ $EXEC_STATUS = 0 ]
then
MESSAGE=$COMPLETEDMSG
else
MESSAGE=`echo $PROBLEMMSG $LOGMSG`
fi
show_status
exit
