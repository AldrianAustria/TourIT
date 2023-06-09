<?php
  $rfid_file = 'rfid.txt';

  if (isset($_POST['input'])) {
    $input = $_POST['input'];
    file_put_contents($rfid_file, (string) $input);
    $rfid = file_get_contents($rfid_file);
    echo "Input received: $rfid";
  } else {
    echo "Input not received";
  }
?> 