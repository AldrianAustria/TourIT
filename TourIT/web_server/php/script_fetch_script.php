<?php
require_once "db_connector.php";

// Get ID from GET parameter
if(isset($_GET["id"])){
    $scriptID = $_GET["id"];

    // Query scripts table for selected script
    $query = "SELECT Script FROM script WHERE Title=\"$scriptID\";";
    $result = mysqli_query($con, $query);
    $row = mysqli_fetch_array($result);
    
    echo $row["Script"];
}
?>