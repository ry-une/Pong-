# Pong

A small Python learning project implementing a two-player Pong game with the `simplegui` API.

## Source

The game is stored in [PongPong](PongPong), an extensionless Python source file. It imports `simplegui` and `random` and defines drawing, keyboard, ball, paddle, score, and reset behavior.

## Controls

| Player / action | Control |
| :--- | :--- |
| Left paddle | W and S |
| Right paddle | Up and Down arrows |
| Reset scores and ball | New Game button |

## Runtime requirements

The source requires an environment implementing the `simplegui` API used in the file. That API is not part of Python's standard library. No dependency manifest or verified local installation procedure is included.

## Known limitations

The paddle update logic uses `if`/`elif`, so updating the left paddle can prevent the right paddle from updating during the same frame. Runtime behavior has not been tested as part of this documentation update.
