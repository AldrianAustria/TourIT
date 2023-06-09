<?php
require_once "db_connector.php";

$rfid_file = 'rfid.txt';
$rfid = file_get_contents($rfid_file);

$query = "SELECT ID FROM `rfid` WHERE RFID = '$rfid';";
$result = mysqli_query($con, $query);

$row = mysqli_fetch_array($result);
    
echo $row["ID"];
?>