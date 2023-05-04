# dimensions to retrieve; assumes (1920,1080) image
# crop region: (left, upper, right, lower)
player_health_crop = (150, 45, 1200, 60)

# threshold of red channel for finding the health bar
threshold_red = (90, 200)
threshold_green = (0, 50)
threshold_blue = (0, 50)

# Player Health Pointer Address
player_pointer_address = 0x7FF7204BCDD8  # WorldChrMan
player_health_offsets = [0x10EF8, 0x00, 0x190, 0x00, 0x138]
