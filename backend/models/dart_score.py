import math

def calculate_dart_score(dartboard, dart, bull=None):
   
    # Calculate dartboard center and radius
    cx = (dartboard["xmin"] + dartboard["xmax"]) / 2
    cy = (dartboard["ymin"] + dartboard["ymax"]) / 2
    radius = (dartboard["xmax"] - dartboard["xmin"]) / 2  # Approximate radius

    # Dart position (center of bounding box)
    dx = (dart["xmin"] + dart["xmax"]) / 2
    dy = (dart["ymin"] + dart["ymax"]) / 2

    # Calculate distance from dartboard center
    distance = math.sqrt((dx - cx) ** 2 + (dy - cy) ** 2)

    # Calculate angle to determine sector
    angle = math.degrees(math.atan2(dy - cy, dx - cx))
    angle = (angle + 360) % 360  # Normalize angle

    # Dartboard numbering order (clockwise from 20)
    dartboard_numbers = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17,
                         3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

    # Determine sector (each segment is 18 degrees)
    segment_index = int((angle + 9) // 18) % 20
    base_score = dartboard_numbers[segment_index]

    # Check for bullseye
    if bull:
        if dart["xmin"] >= bull["xmin"] and dart["xmax"] <= bull["xmax"] and \
           dart["ymin"] >= bull["ymin"] and dart["ymax"] <= bull["ymax"]:
            return 50  # Inner Bullseye

    # Scoring based on distance
    if distance < radius * 0.1:
        return 50  # Inner Bullseye
    elif distance < radius * 0.2:
        return 25  # Outer Bullseye
    elif distance > radius * 0.8:
        return 0  # Outside Dartboard
    elif radius * 0.6 < distance < radius * 0.8:
        return base_score * 2  # Double Ring
    elif radius * 0.4 < distance < radius * 0.6:
        return base_score * 3  # Triple Ring
    else:
        return base_score  # Single Score
