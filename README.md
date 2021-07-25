# TemtemLumaBot

## Info

Uses image recognition and keyboard inputs to find Lumas. Does NOT edit memory or game files.<br/>
Currently only works for grass and cave backgrounds. (Adding the others soon)<br/>
<br/>
Graphical Settings editor may come later too.<br/>

## How to use

Run "python LumaBot.py".<br/>
If you are on windows you can also just run the "run.bat" file.<br/>

## Settings

`
{<br/>
	"resolution": 0,<br/>
	"resList": [<br/>
			[1920,1080],<br/>
			[3440,1440]<br/>
		],<br/>
	"walkTime": 0.1,<br/>
	"reposTime": 25,<br/>
	"lumaCheck": 0.65,<br/>
	"conApi": ""<br/>
}<br/>
`
<br/>
Supports 16:9 and 21:9 formats.<br/>
Change resolution to 0 or 1 respectively.<br/>
<br/>
conApi lets you send the console outputs to a remote server if desired.
