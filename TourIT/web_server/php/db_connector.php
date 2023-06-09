<?php
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "tourit";
    $con = mysqli_connect($servername, $username, $password, $dbname);
    if(!$con){
        die("No Connection: ". mysqli_connect_error());
    }
?>