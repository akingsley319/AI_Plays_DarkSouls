# AI_Plays_DarkSouls

This project seeks to train an AI to face various bosses in the popular FromSoftware games. The goal is to train the AI to beat various bosses throughout the catalogue of From Software games available on the PC platform. These titles include Dark Souls, Dark Souls 3, and Elden Ring. The first title to be attempted is Elden Ring, due to recency and better keyboard & mouse implementation.

This project will focus on beating bosses, and not navigating the world. While the goal is to create an AI that can battle any boss, it is most important to train it to beat a single boss first.

# Object Detection

Object Detection using FasterRCNN was used to reward the AI for keeping the boss on screen, speeding up training while simultaneously rewarding the AI for staying alive. Bounding Box definition was performed manually using Label Studio.

# Image Detection

Various parts of the visible screen are tracked for a variety of purposes. These purposes include starting agent training, restarting the environment, and giving feedback for the purpose of providing rewards and penalties to the agent.

More information on Object Detection and Image Detection, along with various examples, can be found in the *screengrab_configuration* document in the **docs** folder.