# Basketball Simulation

A physics-based basketball simulation game that applies realistic motion physics, interactive shooting mechanics, and visual effects to enhance gameplay. This project uses **Pygame** and **NumPy** for 2D physics modeling, including gravity, collisions, and particle effects.

## **Features**

- **Realistic Physics**: Simulates ball motion with gravity, adjustable friction, and bounce strength, creating an engaging gameplay experience.
- **Collision Detection**: Detects collisions with screen boundaries and court elements, applying a mirrored velocity change for realistic rebounds.
- **Interactive Shooting**: Uses mouse-based shooting with trajectory calculation, allowing players to adjust aim and power.
- **Visual Effects**: Particle trails and explosion animations enhance the experience when a player scores.
- **Performance Monitoring**: Real-time FPS display and adjustable frame rate for consistent gameplay performance.

## **Setup and Installation**

1. **Install Pygame**:
   ```bash
   pip install pygame numpy
   ```

2. **Add Required Assets**: Ensure that `grass.png` is in the same directory as the script, as it’s used for the game background.

3. **Run the Simulation**: Execute the script from your terminal or IDE:
    ```bash
    python basketball.py
    ```

## **Gameplay Instructions**
- **Start**: Run the program to initiate full-screen gameplay.
- **Shoot the Ball**: Click anywhere on the screen to aim and shoot. The ball will move toward the clicked position.
- **Score Points**: Aim for the hoop positioned on the right side of the screen. Scoring triggers an explosion effect.
- **Exit**: Close the game window or press ESC to exit.

## **Configuration**
The following settings can be adjusted in basketball.py:

- **Gravity (`gravity`)**: Controls the downward force applied to the ball.
- **Bounce Strength (`bounce_strength`)**: Adjusts how much the ball rebounds upon impact with surfaces.
- **Frame Rate (`fps`)**: Controls the frames per second to optimize performance.
- **Trail and Particle Effects**: Customize `trail_required_speed` and `trail_cooldown` for trail effects.

## **Dependencies**
- **Pygame**: Handles graphics, game loop, and user input.
- **NumPy**: Provides efficient array operations for physics calculations.
