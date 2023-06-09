<?php
  $battery_file = 'batter.txt';

  if (isset($_POST['input'])) {
    $input = $_POST['input'];
    file_put_contents($battery_file, (string) $input);
    $batt = file_get_contents($battery_file);
    echo "Input received: $batt";
  } else {
    echo "Input not received";
  }
?> 