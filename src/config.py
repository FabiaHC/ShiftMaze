green1 = (155, 188, 15)
green2 = (139, 172, 15)
green3 = (48, 98, 48)
green4 = (15, 56, 15)

tileTypes = {
    "straight_ns": ["N", "S"],  # North-South
    "straight_ew": ["E", "W"],  # East-West
    "T_nes": ["N", "E", "S"],   # T-shape North-East-South
    "T_new": ["N", "E", "W"],   # T-shape North-East-West
    "T_nws": ["N", "W", "S"],   # T-shape North-West-South
    "T_ews": ["E", "W", "S"],   # T-shape East-West-South
    "L_ne" : ["N", "E"],        # L-shape North-East
    "L_nw" : ["N", "W"],        # L-shape North-West
    "L_es" : ["E", "S"],        # L-shape South-East
    "L_ws" : ["W", "S"],        # L-shape South-West

    "goal" : ["N", "E"]        # L-shape North-East (goal)
}

playerSpeed             = 20    # lower means faster
playerAnimationSpeed    = 5    # has to be lower than playerSpeed

xOffset = 160
yOffset = 72


scores = {
    "GOAL" : 1000,
    "GOAL_STEPS" : 1000,
    "MAZE_SHIFTING" : -100,
    "PLAYER_SHIFTING" : -100,
    "GOALSHIFTING" : -100
}
