<?php
function connexion_local_read()
{	
	global $link_ocs,$db_ocs;
	require_once(CONF_MYSQL);
 	//require_once($_SESSION['OCS']['NAME_MYSQL']);
	//connection OCS
	$db_ocs = DB_NAME;
	//lien sur le serveur OCS
	$link_ocs=mysql_connect(SERVER_READ,COMPTE_BASE,PSWD_BASE);

	if(!$link_ocs) {
			echo "<br><center><font color=red><b>ERROR: MySql connection problem<br>".mysql_error()."</b></font></center>";
			die();
		}
	mysql_query("SET NAMES 'utf8'");
	//sql_mode => not strict
	mysql_query("SET sql_mode='NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'");
	//fin connection OCS	
}

function connexion_local_write()
{	
	global $link_ocs,$db_ocs;
	require_once(CONF_MYSQL);
 	//require_once($_SESSION['OCS']['NAME_MYSQL']);
	//connection OCS
	$db_ocs = DB_NAME;
	//lien sur le serveur OCS
	$link_ocs=mysql_connect(SERVER_WRITE,COMPTE_BASE,PSWD_BASE);

	if(!$link_ocs) {
			echo "<br><center><font color=red><b>ERROR: MySql connection problem<br>".mysql_error()."</b></font></center>";
			die();
		}
	mysql_query("SET NAMES 'utf8'");
	//sql_mode => not strict
	mysql_query("SET sql_mode='NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'");
	//fin connection OCS	
}

?>
