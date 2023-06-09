<?php
require_once "db_connector.php";

// Get ID and script from POST parameters
$scriptID = $_POST["id"];
$script = $_POST["script"];

// Update script in scripts table
$query = "UPDATE script SET Script='" . $script . "' WHERE Title=\"$scriptID\"";
if (mysqli_query($con, $query)) {
	echo "Script updated successfully";
} else {
	echo "Error updating script: " . mysqli_error($conn);
}

mysqli_close($con);

?>