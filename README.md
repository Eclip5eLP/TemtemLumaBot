# TemtemLumaBot

## Info

Uses image recognition and keyboard inputs to find Lumas. Does NOT edit memory or game files.<br/>
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
    "reposType": 0,      // 0 - Dont reposition, 1 - Automatic repositioning, 2 - Automatic repositioning but manual on fail
    "walkTime": [        // Time to walk into a direction
        0.2,             // Left
        0.2              // Right
    ],
    "reposTime": 30.0,   // Time to try repositioning before acting again
    "lumaCheck": 0.55,   // Image recognition threshold (0 - 1)
    "pattern": 0,        // Active pattern (0, 1, 2)
    "patternList": [     // Search and walking pattern
        "fast",          // 0 - Find Battle fast
        "random",        // 1 - Run around randomly
        "real"           // 2 - Imitate real player (not implemented yet)
    ],
    "controls": {
        "exit": "1",     // Stop Bot
        "pause": "p",    // Pause Bot until pressed again
        "hold": "0",     // Pause Bot while holding this key
        "left": "a",
        "right": "d",
        "up": "w",
        "down": "s"
    }
}
```
