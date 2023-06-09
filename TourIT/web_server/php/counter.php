<?php
  $count_file = 'count.txt';
  require_once "db_connector.php";

  if (isset($_POST['input'])) {
    $num = $_POST['input'];
    $query = "UPDATE `people_counter` SET `people_count` = $num WHERE `people_counter`.`ID` = 1;";
    mysqli_query($con, $query);
  } else {
    echo "Input not received";
  }
?> 