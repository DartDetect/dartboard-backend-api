import math

# Standard dartboard dimensions for scaling (in mm)
DARTBOARD_DIAMETER = 340  # Actual steel-tip dartboard diameter
BULLSEYE_RADIUS = 6.35  # Inner bull radius
OUTER_BULL_RADIUS = 15.875  # Outer bull radius
TRIPLE_RING_INNER = 107.95  # Inner edge of triple ring
TRIPLE_RING_OUTER = 114.3  # Outer edge of triple ring
DOUBLE_RING_INNER = 170  # Inner edge of double ring
DOUBLE_RING_OUTER = 176.35  # Outer edge of double ring

# Correct dartboard numbering (clockwise from top center 20)
SECTION_SCORES = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 
                  3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

def calculate_dart_score(dartboard, dart, bull=None):
    """
    Improved dart scoring using the dart bounding box center.
    """
    # **Get Dartboard Bounding Box**
    x1, y1, x2, y2 = dartboard["xmin"], dartboard["ymin"], dartboard["xmax"], dartboard["ymax"]
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    detected_dartboard_diameter = max(x2 - x1, y2 - y1)
    scale_factor = DARTBOARD_DIAMETER / detected_dartboard_diameter  # Normalize to actual dartboard size

    # **Get Dart Bounding Box Center**
    dart_x = (dart["xmin"] + dart["xmax"]) / 2
    dart_y = (dart["ymin"] + dart["ymax"]) / 2

    # **Normalize position relative to dartboard center**
    rel_x = (dart_x - center_x) * scale_factor
    rel_y = (dart_y - center_y) * scale_factor
    distance = math.hypot(rel_x, rel_y)

    # **Compute Sector Angle (Fix alignment)**
    angle = (math.degrees(math.atan2(rel_y, rel_x)) + 270) % 360  
    adjusted_angle = (angle - 9) % 360  # **FIX**: Fine-tune sector alignment
    sector_index = int(adjusted_angle // 18) % 20  
    base_score = SECTION_SCORES[sector_index]

    # 🔍 **Debugging Output**
    print("\n--- Dart Scoring Debugging ---")
    print(f"🎯 Dart Center Position: ({dart_x:.2f}, {dart_y:.2f})")
    print(f"📍 Dartboard Center: ({center_x:.2f}, {center_y:.2f})")
    print(f"📍 Relative Position (normalized): ({rel_x:.3f}, {rel_y:.3f})")
    print(f"📍 Distance from Center: {distance:.3f}")
    print(f"📍 Angle: {angle:.2f}° (Adjusted: {adjusted_angle:.2f}°)")
    print(f"Sector Index: {sector_index}, Base Score: {base_score}")

    # **Check if the dart is in the bullseye**
    if bull:
        bull_x = (bull["xmin"] + bull["xmax"]) / 2
        bull_y = (bull["ymin"] + bull["ymax"]) / 2
        bull_radius = ((bull["xmax"] - bull["xmin"]) + (bull["ymax"] - bull["ymin"])) / 4

        # Check if the dart is within the bullseye
        if math.hypot(dart_x - bull_x, dart_y - bull_y) <= bull_radius:
            if distance <= BULLSEYE_RADIUS:
                print(f"Inner Bullseye! Score: 50")
                return 50
            elif distance <= OUTER_BULL_RADIUS:
                print(f"Outer Bullseye! Score: 25")
                return 25

    # **Check if the dart is in the triple or double ring**
    if TRIPLE_RING_INNER <= distance <= TRIPLE_RING_OUTER:
        print(f"Triple Ring! Score: {base_score * 3}")
        return base_score * 3
    elif DOUBLE_RING_INNER <= distance <= DOUBLE_RING_OUTER:
        print(f"Double Ring! Score: {base_score * 2}")
        return base_score * 2
    elif distance > DOUBLE_RING_OUTER:
        print("❌ Missed Dartboard! Score: 0")
        return 0

    # **Default single score**
    print(f"✅ Single Score: {base_score}")
    return base_score
