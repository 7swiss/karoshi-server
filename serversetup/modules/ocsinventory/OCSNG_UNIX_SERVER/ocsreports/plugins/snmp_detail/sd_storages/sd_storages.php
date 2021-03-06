<?php
//====================================================================================
// OCS INVENTORY REPORTS
// Copyleft Erwan GOALOU 2010 (erwan(at)ocsinventory-ng(pt)org)
// Web: http://www.ocsinventory-ng.org
//
// This code is open source and may be copied and modified as long as the source
// code is always made freely available.
// Please refer to the General Public Licence http://www.gnu.org/ or Licence.txt
//====================================================================================

print_item_header('sd_storages');
	if (!isset($protectedPost['SHOW']))
		$protectedPost['SHOW'] = 'NOSHOW';
	$form_name="sd_storages";
	$table_name=$form_name;
	echo "<form name='".$form_name."' id='".$form_name."' method='POST' action=''>";
	$list_fields=array('SNMP_ID' => 'SNMP_ID',
					'MANUFACTURER'=> 'MANUFACTURER',
					'NAME'        =>  'NAME'   ,
					'MODEL'        => 'MODEL'   ,
					'DESCRIPTION'  => 'DESCRIPTION'  ,
					'TYPE'         => 'TYPE'  ,
					'DISKSIZE'     => 'DISKSIZE' ,
					'SERIALNUMBER' => 'SERIALNUMBER',
					'FIRMWARE'     => 'FIRMWARE'
					   );
	//$list_fields['SUP']= 'ID';
	$list_col_cant_del=$list_fields;
	$default_fields= $list_fields;
	$sql=prepare_sql_tab($list_fields);
	$sql['SQL']  = $sql['SQL']." FROM %s WHERE (snmp_id=%s)";
	$sql['ARG'][]='snmp_storages';
	$sql['ARG'][]=$systemid;
	$tab_options['ARG_SQL']=$sql['ARG'];
	tab_req($table_name,$list_fields,$default_fields,$list_col_cant_del,$sql['SQL'],$form_name,80,$tab_options);
	echo "</form>";


?>