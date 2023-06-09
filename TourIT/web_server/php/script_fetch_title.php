<?php
require_once "db_connector.php";

// Get ID from GET parameter
$scriptID = $_GET["id"];

// Query scripts table for selected script
$query = "SELECT Title FROM script WHERE Title=" . $scriptID;
$result = mysqli_query($con, $query);
$row = mysqli_fetch_array($result);

echo $row["Title"];
?>