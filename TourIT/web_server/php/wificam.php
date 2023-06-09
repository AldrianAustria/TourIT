<?php
// $stream_url = "http://192.168.1.8/1280x720.jpg"; // Replace with your ESP32 camera's IP address and port number
// header('Content-Type: image/jpeg');
// $stream = fopen($stream_url, 'rb');
// if ($stream) {
//     fpassthru($stream);
// } else {
//     echo "Failed to open stream to $stream_url";
// }
$stream_url = "http://192.168.1.8/1280x720.mjpeg"; // Replace with your ESP32 camera's IP address and port number
header("Content-Type: multipart/x-mixed-replace; boundary=frame");
$stream = fopen($stream_url, 'r');
if ($stream) {
    while (true) {
        $buffer = '';
        while (($char = fgetc($stream)) !== false) {
            $buffer .= $char;
            if (strpos($buffer, "\r\n\r\n") !== false) {
                break;
            }
        }
        $headers = trim($buffer);
        $header_array = explode("\r\n", $headers);
        foreach ($header_array as $header) {
            header($header);
        }
        fpassthru($stream);
        //usleep(10000); // Adjust this to change the rate at which frames are fetched from the camera
    }
} else {
    echo "Failed to open stream to $stream_url";
}

?>
