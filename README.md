# TemtemLumaBot

## Info

Uses image recognition and keyboard inputs to find Lumas. Does NOT edit memory or game files.
Currently only works for grass and cave backgrounds. (Adding the others soon)

Graphical Settings editor may come later too.

## How to use

Run "python LumaBot.py".
If you are on windows you can also just run the "run.bat" file.

## Settings

`
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
`

Supports 16:9 and 21:9 formats.
Change resolution to 0 or 1 respectively.

conApi lets you send the console outputs to a remote server if desired.
