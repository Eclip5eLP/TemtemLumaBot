# TemtemLumaBot

## Info

Uses image recognition and keyboard inputs to find Lumas. Does NOT edit memory or game files.<br/>
Currently only works for grass and cave backgrounds. (Adding the others soon)<br/>
<br/>

## How to use

Run ```python LumaBot.py``` in your terminal.<br/>
If you are on windows you can also just execute the ```run.bat``` file.<br/>
<br/>
Bot Controls:<br/>
```
Q - Stop
P - Pause
```

## Settings

```
{
    "resolution": 0,
    "resList": [
        [
            1920,
            1080
        ],
        [
            3440,
            1440
        ]
    ],
    "walkTime": 0.1,
    "reposTime": 30.0,
    "lumaCheck": 0.65,
    "pattern": 0,
    "patternList": [
        "fast",
        "random",
        "real"
    ],
    "conApi": ""
}
```
<br/>
Supports 1920x1080 and 3440x1440 resolutions.<br/>
Change resolution to 0 or 1 respectively.<br/>
<br/>
conApi lets you send the console outputs to a remote server if desired.

## Server API for output

This is a possible solution for an API that accepts the bots output and saves it in a file on the server.

```
<?php
//Log to Terminal
if (isset($_GET["log"])) {
	if (isset($_GET["app"])) {
		$file = "terminal.log";

		//Read
		$cont = "";
		if (file_exists($file)) $cont = file_get_contents($file);

		//Fix output (Bot Output includes terminal color coding, this removes that)
		$output = preg_replace("/[[:cntrl:]]/", "", $_GET["log"]);
		$output = preg_replace('/\[..m/i', '', $output);
		
		//Write
		$date = date('Y-m-d H:i:s');
		$cont = $cont."[".$_GET["app"]."](".$date.") ".$output."&#13;&#10;";
		$fp = fopen($file, "w");
  		fwrite($fp, $cont);
  		fclose($fp);

  		echo "200";
	}
}
?>
```
