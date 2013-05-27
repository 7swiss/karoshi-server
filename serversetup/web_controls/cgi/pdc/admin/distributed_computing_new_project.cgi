#!/bin/bash
#Copyright (C) 2013 Robin McCorkell
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
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
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/distributed-computing/new_project ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/system/distributed-computing/new_project
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
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>'$TITLE'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi">
<link rel="stylesheet" href="/css/'$STYLESHEET'"><script src="/all/stuHover.js" type="text/javascript"></script>
</head><body>'

#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:\-' | sed 's/__/_ _/g'`

#########################
#Assign data to variables
#########################
END_POINT=7
function assign_data_variable {
	[ "$1" ] || return
	COUNTER=2
	while [ $COUNTER -le $END_POINT ]; do
		DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
		if [ "$DATAHEADER" = "$1" ]; then
			let COUNTER=$COUNTER+1
			eval $1=`echo $DATA | cut -s -d'_' -f$COUNTER`
			break
		fi
		let COUNTER=$COUNTER+1
	done
}
assign_data_variable PROJECTTYPE
assign_data_variable PROJECTNAME
assign_data_variable DATAFILE

STARTCGI=distributed_computing_new_project_fm.cgi

function show_status {
echo '<script type="text/javascript">'
echo 'alert("'$MESSAGE'");'
echo 'window.location = "/cgi-bin/admin/'$STARTCGI'";'
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
if [ ! -f /opt/karoshi/web_controls/web_access_admin ] || [ -z "$REMOTE_USER" ]
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
function error_if_empty {
	if [ -z "${!1}" ]; then
		MESSAGE="$2"
		show_status
	fi
}
error_if_empty PROJECTTYPE "$ERRORMSG1"
error_if_empty PROJECTNAME "$ERRORMSG1"

#Check if project type is an actual type
if [ ! -f /home/distributed-computing/project-types/"$PROJECTTYPE" ]; then
	MESSAGE="$ERRORMSG2"
	show_status
fi

#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin


echo '</body></html>'
exit

