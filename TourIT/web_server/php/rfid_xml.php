<?php
require_once "db_connector.php";

$rfid_file = 'rfid.txt';
$rfid = file_get_contents($rfid_file);

$query = "SELECT ID FROM `rfid` WHERE RFID = '$rfid';";
$result = mysqli_query($con, $query);

if($result->num_rows == 0){
    $doc = new DOMDocument();
    $root = $doc->createElement('data');
    $doc->appendChild($root);

    // Add the data to the XML document
    $item = $doc->createElement('item');
    $element = $doc->createElement('ID', 'NULL');
    $item->appendChild($element);
    $root->appendChild($item);
    header('Content-Type: application/xml');
    echo $doc->saveXML();
}else{
    // Create a new XML document
    $doc = new DOMDocument();
    $root = $doc->createElement('data');
    $doc->appendChild($root);

    // Add the data to the XML document
    while ($row = $result->fetch_assoc()) {
        $item = $doc->createElement('item');

        foreach ($row as $key => $value) {
            $element = $doc->createElement($key, $value);
            $item->appendChild($element);
        }
    $root->appendChild($item);
    }
    header('Content-Type: application/xml');
    echo $doc->saveXML();
}
?>