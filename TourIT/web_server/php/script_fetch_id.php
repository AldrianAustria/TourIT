<?php
require_once "db_connector.php";

$query = "SELECT Title FROM script";
$result = mysqli_query($con, $query);

// Populate dropdown menu with IDs
while ($row = mysqli_fetch_array($result)) {
	echo "<option value=\"" . $row["Title"] . "\">" . $row["Title"] . "</option>";
}
?>