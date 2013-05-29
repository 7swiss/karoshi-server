#!/usr/bin/env perl
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

use lib '/opt/karoshi/web_controls/perl_mods';

use CGI;
$CGI::POST_MAX=1024 * 1024 * 8; # 8MiB uploads
use ParseBash;
use File::Spec;

my $query = CGI->new;
my $bashVars = ParseBash->new;

############################
#Language
############################
$bashVars->var('LANGUAGE', "englishuk");
$bashVars->var('STYLESHEET', "defaultstyle.css");
$bashVars->var('TIMEOUT', 300);
$bashVars->var('NOTIMEOUT', "127.0.0.1");
$bashVars->parseFile('/opt/karoshi/web_controls/user_prefs/' . $query->remote_user());
$bashVars->parseFile('/opt/karoshi/web_controls/language/englishuk/distributed_computing/new_project');
$bashVars->parseFile('/opt/karoshi/web_controls/language/' . $bashVars->var('LANGCHOICE') . '/distributed_computing/new_project');
$bashVars->parseFile('/opt/karoshi/web_controls/language/englishuk/all');
$bashVars->parseFile('/opt/karoshi/web_controls/language/' . $bashVars->var('LANGCHOICE') . '/all');

#Check if timout should be disabled
if ($bashVars->var('NOTIMEOUT') =~ /\Q${\$query->remote_addr()}\E/) {
	$bashVars->var('TIMEOUT', 86400);
}

#Detect mobile browser
my $isMobile = $query->user_agent(Mobi) or $query->user_agent(Mini);

############################
#Show page
############################
print $query->header(-charset => 'utf-8');

my @stylesheets = ({-src => '/css/' . $bashVars->var('STYLESHEET')});
my @scripts = ({-src => '/all/stuHover.js' });
my @metas = ($query->meta({-http_equiv => 'CACHE-CONTROL', -content => 'NO-CACHE'}));

if ($isMobile) {
	push (@stylesheets, { -src => "/all/mobile_menu/sdmenu.css" });
	push (@scripts, { -src => "/all/mobile_menu/sdmenu.js" });
	push (@scripts, { -script => "var myMenu; window.onload = function() { myMenu = new SDMenu('my_menu'); myMenu.init(); };" });
}
push (@metas, $query->meta({-http_equiv => 'REFRESH', -content => $bashVars->var('TIMEOUT')}));

print $query->start_html(-title => $bashVars->var('TITLE'), -style => \@stylesheets, -script => \@scripts, -head => \@metas);

#Error handling
my $startPage = 'distributed_computing_new_project_fm.cgi';

sub show_status {
	my $message = @_ ? shift : $bashVars->var('PROBLEMMSG');
	$message = $message ? $message : $bashVars->var('PROBLEMMSG');
	print $query->script({-type=>'text/javascript'},
		"\n",
		"alert('" . $message . "');\n",
		"window.location = '/cgi-bin/admin/" . $startPage . "';\n",
		"</script>\n"),
		$query->end_html;
	exit;
}

#Check for CGI errors
show_status $query->cgi_error if $query->cgi_error;

#########################
#Access control
#########################
#Check https access
show_status $bashVars->var('HTTPS_ERROR') unless $query->https;

#Check user accessing this script
show_status $bashVars->var('ACCESS_ERROR1') unless $query->remote_user and open my $accessFile, '/opt/karoshi/web_controls/web_access_admin';
my $userPermitted = 0;
while (my $line = <$accessFile> ) {
	if ( $line =~ /^\Q${\$query->remote_user}\E:/ ) {
		$userPermitted = 1;
		last;
	}
}
show_status $bashVars->var('ACCESS_ERROR1') unless $userPermitted;

#########################
#Generate content
#########################
my @projectTypeArray = map { (File::Spec->splitpath($_))[2] } glob("/home/distributed_computing/project_types/*");
push(@projectTypeArray, $bashVars->var('NOTYPES')) if not @projectTypeArray;

my $divType;
my @pageStructure;
if ($isMobile) {
	$divType = 'mobileactionbox';
	#Generate back button
	print $query->div({ -style => "float: left;", -id => "my_menu", -class => "sdmenu" },
		$query->div({ -class => "expanded" },
			$query->span($bashVars->var('TITLE')),
			$query->a({ -href => "/cgi-bin/admin/mobile_menu.cgi" }, $bashVars->var('DISTRIBUTEDMENUMSG'))));
	push(@pageStructure, $bashVars->var('PROJECTNAME'), $query->br);
	push(@pageStructure, $query->textfield( -name => "projectName", -style => 'width: 350px;', -size => 30 ), $query->br);
	push(@pageStructure, $bashVars->var('PROJECTTYPE'), $query->br);
	push(@pageStructure, $query->popup_menu( -name => "projectType", -values => \@projectTypeArray, -style => 'width: 350px;' ), $query->br);
	push(@pageStructure, $bashVars->var('DATAFILE'), $query->br);
	push(@pageStructure, $query->filefield( -name => "dataFile", -style => 'width: 350px;', -size => 30 ), $query->br);
	push(@pageStructure, $query->submit( -value => $bashVars->var('SUBMITMSG') ), $query->reset( -value => $bashVars->var('RESETMSG') ) );
} else {
	$divType = 'actionbox';
	#Generate navigation bar
	system('/opt/karoshi/web_controls/generate_navbar_admin');
	push(@pageStructure, $query->b($bashVars->var('TITLE')), $query->br, $query->br);
	push(@pageStructure, $query->table({ -class=>"standard", -style=>"text-align: left;", -border=>"0", -cellpadding=>"2", -cellspacing=>"2" },
		$query->Tr(
			$query->td({ -style=>"width: 180px;" }, $bashVars->var('PROJECTNAME') ),
			$query->td(
				$query->textfield( -name => "projectName", -style => 'width: 350px;', -size => 30 )),
			$query->td(
				$query->a({ -class => "info", -target => "_blank", -href => "http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Distributed_Computing" },
					$query->img({ -class => "images", -alt => "", -src => "/images/help/info.png" },
						$query->span($bashVars->var('PROJECTNAMEHELP')))))),
		$query->Tr(
			$query->td({ -style=>"width: 180px;" }, $bashVars->var('PROJECTTYPE') ),
			$query->td(
				$query->popup_menu( -name => "projectType", -values => \@projectTypeArray, -style => 'width: 350px;' )),
			$query->td(
				$query->a({ -class => "info", -target => "_blank", -href => "http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Distributed_Computing" },
					$query->img({ -class => "images", -alt => "", -src => "/images/help/info.png" },
						$query->span($bashVars->var('PROJECTTYPEHELP')))))),
		$query->Tr(
			$query->td({ -style=>"width: 180px;" }, $bashVars->var('DATAFILE') ),
			$query->td(
				$query->filefield( -name => "dataFile", -style => 'width: 350px;', -size => 30 )),
			$query->td(
				$query->a({ -class => "info", -target => "_blank", -href => "http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Distributed_Computing" },
					$query->img({ -class => "images", -alt => "", -src => "/images/help/info.png" },
						$query->span($bashVars->var('DATAFILEHELP')))))) ));
}

print $query->start_multipart_form( -action => "/cgi-bin/admin/distributed_computing_new_project.cgi" );

print $query->div( {-id=>$divType},
	@pageStructure);
	
#Desktop version uses 'submitbox' div to contain submit and reset buttons
print $query->div( {-id=>'submitbox'},
	$query->submit( -value => $bashVars->var('SUBMITMSG') ),
	$query->reset( -value => $bashVars->var('RESETMSG') )) if not $isMobile;

print $query->end_form;
	
print $query->end_html;