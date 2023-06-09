<?php
require_once "db_connector.php";


$query = "SELECT loc FROM `location` WHERE id = '1';";
$result = mysqli_query($con, $query);

$row = mysqli_fetch_array($result);
    
echo $row["loc"];
?>