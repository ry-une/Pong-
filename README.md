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

## Game-state walkthrough

The following describes [PongPong](PongPong) by source inspection; it is not a report of a successful game session.

| Function | Responsibility |
| :--- | :--- |
| spawn_ball(direction) | Places the ball at the center and chooses a random upward velocity, with horizontal direction determined by the argument. |
| new_game() | Clears both scores, restores paddle positions, and serves the ball to the left. |
| draw(canvas) | Advances positions, checks walls and paddle gutters, updates scores, and renders the frame. |
| keydown(key) | Sets the appropriate paddle velocity from the movement key. |
| keyup(key) | Zeros the corresponding paddle velocity when its movement key is released. |

The source creates a 600 by 400 canvas, registers draw and keyboard handlers, adds the New Game button, calls new_game(), and starts the frame.

### Scoring and speed

- A miss at the right gutter increments the left player's score and respawns the ball heading left. A miss at the left gutter increments the right player's score and respawns it heading right.
- A successful paddle hit increases the magnitude of horizontal velocity by 20 percent. Vertical wall contact reverses vertical velocity.
- Movement is advanced once per draw callback, without elapsed-time scaling. Observed speed therefore depends on the environment's callback timing.

### Reset and keyboard edge cases

Although new_game() declares the paddle velocity globals, it does not assign zero to them. A reset can therefore retain an existing movement velocity until a later key event changes it. The reset is not a full reset of all game state.

Key release also zeros the paddle velocity without tracking whether the opposite movement key remains held. This matters when testing overlapping key presses. Together with the existing if/elif limitation, these are useful cases for a future code-fix task.

When reproducing a behavior, record the runtime implementation, version, exact key sequence, whether New Game was clicked while a movement velocity was active, and the observed paddle and score state. A missing simplegui import is an environment/setup failure, not evidence that collision or scoring logic was exercised.
