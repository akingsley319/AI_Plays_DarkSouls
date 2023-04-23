# AI_Plays_DarkSouls

This project seeks to train an AI to face various bosses in the popular FromSoftware games. The goal is to train the AI to beat various bosses throughout the catalogue of From Software games available on the PC platform. These titles include Dark Souls, Dark Souls 3, and Elden Ring. The first title to be attempted is Elden Ring, due to recency and better keyboard & mouse implementation.

This project will focus on beating bosses, and not navigating the world. While the goal is to create an AI that can battle any boss, it is most important to train it to beat a single boss first.

# Object Detection

Object Detection using FasterRCNN was used to reward the AI for keeping the boss on screen, speeding up training while simultaneously rewarding the AI for staying alive. Bounding Box definition was performed manually using Label Studio.

# Image Detection

Various parts of the visible screen are tracked for a variety of purposes. These purposes include starting agent training, restarting the environment, and giving feedback for the purpose of providing rewards and penalties to the agent.

More information on Object Detection and Image Detection, along with various examples, can be found in the *screengrab_configuration* document in the **"docs"** folder.

# AI Plays Elden Ring

I used stable-baselines 3 and open-ai gym to handle the reinforcement learning section, incorporating a PyTorch base for the Neural Network. A PPO Algorithm is applied, with a CNN Policy for image capture. Multiple observations are stacked to display more information from images that are gray-scaled and reduced in size from preprocessing.

As for most reinforcement learning models, the main difficulties come from the reward and penalty system, model hyperparameters, and time. Time has proven to be the most difficult so far.

Due to the game setup, there is not much in terms of speeding up gameplay to force calculations at a faster rate. Even if there was, I have found resetting the boss to be the primary issue that needs to be addressed. Unfortunately, the reset method currently involves waiting for the game to load after player death, quitting to the main menu, replacing the save state in the game folder, loading the game back up, and then entering the boss arena. I am currently exploring cheat engine construction to figure out how to do this more efficiently, without constantly reloading the game, which has been resulting in crashes after approximately 2 hours of training. This is a compromise I am willing to maintain, considering I wanted to avoid cheat engines as much as possible to limit the potential for bans from the online features of Elden Ring, as well as to restrict the AI to the same limitations a human player would have.

## Rewards and Penalties

At this moment, the rewards are outlines as followed, and are subject to change when training can occur at a more consistent pace.

* Maintaining the boss on screen: The boss detection model discussed earlier calculates a confidence score for the boss being on screen. Depending on this score, a minimum and maximum value is set such that the model will be rewarded logarithmically between these two values. If the boss detection model does not meet a designated threshold score (maintained to limit false positives), the minimum value is provided to reward the AI for staying alive.
* Landing a hit on the boss: The image detection model discussed above will look for damage values which are displayed on screen. The model will store these values so that they are not double counted. Each hit will provide a reward proportional to the damage dealt.

Penalties are also important, but are limited to when damage is dealt to the player and death. Damage dealt to the player is tracked through observing the pixel information regarding the health bar. If the width of bar decrease, a penalty is applied proportional to the number of pixels that it decreased.

## Action Space

The action space is currently defined as a Box object (continuous variables within designated ranges). There are 5 outputs expected.

* The first and second outputs control the camera, outputting a value between -1 and positive 1, to indicate range of movement.
* The third and fourth outputs control movement. The keyboard traditionally designates the "a" and "d" keys to move left and right respectively at a constant rate. The values therefore are rounded such that they will output a desired value.
* The final output is used to choose which action to take, also rounding the output value so that one of the following actions are taken:
    * No action
    * Light Attack
    * Strong/Heavy Attack
    * Jump
    * Dodge
    * Use Consumable Action

# Expectations

While the code within is functional, it is not optimal for what I would like to accomplish. I will concede my reservations on learning out to manipulate game stored variables to ensure proper training without the fear of crashing, but hope to maintain my other methods of rewarding and penalizing the AI.