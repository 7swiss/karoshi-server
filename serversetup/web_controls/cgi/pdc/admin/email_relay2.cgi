#!/bin/bash
#Add user
#Copyright (C) 2007  The karoshi Team

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
#  _RELAY_
#  _RADDRESS_
############################
#Language
############################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/email/email_relay ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/email/email_relay
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all

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
END_POINT=4
#Assign RELAY
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = RELAYcheck ]
then
let COUNTER=$COUNTER+1
RELAY=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done
#Assign RADDRESS
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = RADDRESScheck ]
then
let COUNTER=$COUNTER+1
RADDRESS=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

function show_status {
echo '<SCRIPT lang
uage="Javascript">'
echo 'alert("'$MESSAGE'")';
echo '</script>'
echo "</body></html>"
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
#Check to see that RELAY is not blank
if [ $RELAY'null' = null ]
then
MESSAGE=$ERRORMSG1
show_status
fi
#Check to see that RELAY is set to direct or relay
if [ $RELAY != direct ] && [ $RELAY != relay ]
then
MESSAGE=$ERRORMSG2
show_status
fi
#Check to see that relay address is not blank
if [ $RELAY = relay ]
then
if [ $RADDRESS'null' = null ]
then
MESSAGE=$ERRORMSG3
show_status
fi
fi

MD5SUM=`md5sum /var/www/cgi-bin_karoshi/admin/email_relay2.cgi | cut -d' ' -f1`
#Make changes
sudo -H /opt/karoshi/web_controls/exec/email_relay $REMOTE_USER:$REMOTE_ADDR:$MD5SUM:$RELAY:$RADDRESS
if [ $RELAY = direct ]
then
MESSAGE=$COMPLETEDMSG1
else
MESSAGE=`echo $COMPLETEDMSG2 $RADDRESS`
fi
show_status
exit
