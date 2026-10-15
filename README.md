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

## Movement and reset behavior

Both paddles update independently during each draw callback and are clamped to the canvas boundaries. Holding both movement keys for one paddle cancels its movement; releasing either key resumes the direction still held. Repeated keydown events do not accumulate movement state.

New Game clears scores, recorded held keys, and paddle velocities, restores paddle positions, and serves the ball to the left. A subsequent movement-key event can start motion again.

## Game-state walkthrough

The following describes [PongPong](PongPong) by source inspection; it is not a report of a successful game session.

| Function | Responsibility |
| :--- | :--- |
| spawn_ball(direction) | Places the ball at the center and chooses a random upward velocity, with horizontal direction determined by the argument. |
| new_game() | Clears scores, held-key state, and velocities; restores paddle positions and serves left. |
| draw(canvas) | Advances positions, checks walls and paddle gutters, updates scores, and renders the frame. |
| keydown(key) | Records a movement key and recalculates both paddle velocities. |
| keyup(key) | Releases a recorded key and recalculates velocities from keys still held. |
| update_paddle_velocities() | Resolves held keys into independent paddle velocities. |

The source creates a 600 by 400 canvas, registers draw and keyboard handlers, adds the New Game button, calls new_game(), and starts the frame.

### Scoring and speed

- A miss at the right gutter increments the left player's score and respawns the ball heading left. A miss at the left gutter increments the right player's score and respawns it heading right.
- A successful paddle hit increases the magnitude of horizontal velocity by 20 percent. Vertical wall contact reverses vertical velocity.
- Movement is advanced once per draw callback, without elapsed-time scaling. Observed speed therefore depends on the environment's callback timing.

## Regression tests

With Python 3 installed, run from the repository root:

```sh
python -m unittest discover -s tests -v
```

The eight tests execute the actual game handlers through a display-free `simplegui` adapter. They cover simultaneous movement, opposing keys and key release, repeated keydown, reset, boundary clamping, unrelated keys, scoring on both sides, and paddle-hit acceleration. The suite was run with Python 3.12.

The adapter does not test a real `simplegui` window, rendering, focus loss, or operating-system keyboard delivery. Manual play in a compatible runtime remains necessary. Timing still depends on draw callbacks, and the collision implementation is unchanged. When reporting a problem, include the runtime/version, exact key sequence, and observed paddle/score state.
