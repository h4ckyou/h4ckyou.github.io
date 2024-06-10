<?php

function calcul_main($puissance){
  preg_match_all("/{{([^}]*)}}/", $puissance, $original);
$first = array($original[1][0]);
foreach ($first as &$cal){
 $puissance = str_replace("{{" . $cal . "}}", eval("return " . $cal . ";"), $puissance);
}
 return $puissance;
}

function result($puissance) {
    $lines = explode("\n", $puissance);
    $result = array();
    foreach ($lines as $line) {
        $values = explode(":",$line);
        print("La centrale n°".$values[0]." a été enrégistrée avec une puissance de ".$values[1]." watts (W) et sera disponible pendant exactement 15 seconde");
        print(" ID de l'enregistrement = ".mt_rand(10000000, 99999999));
    }
    return $result;
}

if ($_SERVER['REQUEST_METHOD'] == "POST"){
  if (isset($_POST['puissance'])){
//HLB2024{_you_are_on_the_right_track_8796}
    $puissance = trim(calcul_main($_POST['puissance']));
    $puissance = str_replace("\r\n", "\n", $puissance);
//Calcule de puissance thermique

    result($puissance);
  }
  else{
    die("Entrer les informations de la centrale");
  }
}

?>
