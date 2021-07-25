# TemtemLumaBot

## Info

Uses image recognition and keyboard inputs to find Lumas. Does NOT edit memory or game files.<br/>
Currently only works for grass and cave backgrounds. (Adding the others soon)<br/>
<br/>
Graphical Settings editor may come later too.<br/>

## How to use

Run "python LumaBot.py".<br/>
If you are on windows you can also just run the "run.bat" file.<br/>
<br/>
Bot Controls:<br/>
Q - Stop<br/>
P - Pause

## Settings

```
{
	"resolution": 0,
	"resList": [
		[1920,1080],
		[3440,1440]
	],
	"walkTime": 0.1,
	"reposTime": 25,
	"lumaCheck": 0.65,
	"conApi": ""
}
```
<br/>
Supports 1920x1080 and 3440x1440 resolutions.<br/>
Change resolution to 0 or 1 respectively.<br/>
<br/>
conApi lets you send the console outputs to a remote server if desired.
