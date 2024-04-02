import os.path

from helpers import *
from visualizators import *

TAG = '[DETECTOR]'

# Normalize coordinates by lowest X and Y
def normalize_coordinates(points):
    shift = [min([p[0] for p in points]), min([p[1] for p in points])]
    normalized_points = points.copy()

    for i in range(len(points)):
        normalized_points[i] = np.subtract(points[i], shift)

    return normalized_points, shift

def find_holes_coordinates_on_image(img_path: str, mask_type: str):
    try:
        image = cv2.imread(img_path)
    except Exception as e:
        assert False, f'{TAG} Error: error while opening image. Probably path does not exist. Path: \'{img_path}\'\nTraceback: {e}'
    assert image is not None and image.size != 0, f'{TAG} Error: error while reading image. Image is empty. Path: \'{img_path}\''

    # Apply mask
    if mask_type == 'blue':
        masked_image = cv2.inRange(image, blue_lower, blue_upper)
    elif mask_type == 'red':
        masked_image = cv2.inRange(image, red_lower, red_upper)
    else:
        assert False, f'{TAG} Error: no suitable masks was found for \'{mask_type}\''

    # Blur image
    blurred_image = cv2.medianBlur(masked_image, 11)

    # Find contours and draw them
    try:
        contours, _ = cv2.findContours(blurred_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    except Exception as e:
        assert False, f'{TAG} Error: error while finding contours.\nTraceback: {e}'

    assert len(contours) > 0, f'{TAG} Error: no contours were found, ensure you are using appropriate mask! Path: {img_path}; Mask: {mask_type}'

    # Find contours centers and draw them
    try:
        centers = []
        for cnt in contours:
            M = cv2.moments(cnt)
            center = [int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])]
            centers.append(center)
    except Exception as e:
        assert False, f'{TAG} Error: error while calculating contours on image. Path: {img_path}\nTraceback: {e}'

    if DEBUG_VISUALIZE_FOUND_CONTOURS:
        visualize_contours(image, contours, centers)

    return sorted(centers)

def match_coordinates(points1: list, points2: list):
    assert len(points1) == len(points2), f'{TAG} Error: number of holes on images doesn`t match: {len(points1)} and {len(points2)}.'

    # Normalize points
    try:
        normalized_p1, shift1 = normalize_coordinates(points1.copy())
        normalized_p2, shift2 = normalize_coordinates(points2.copy())
    except Exception as e:
        assert False, f'{TAG} Error: error on normalizing coordinates.\nTraceback: {e}'

    pairs = [points1, []]

    # Go by sorted coordinates and find its pairs, while deleting every found pair points to avoid N:1 matches
    try:
        for np1_i in normalized_p1:
            ind = get_index_of_closest_point(normalized_p2, np1_i)
            pairs[1].append(points2[ind])
            points2.pop(ind), normalized_p2.pop(ind)
    except Exception as e:
        assert False, f'{TAG} Error: error on matching coordinates pairs.\nTraceback: {e}'

    if DEBUG_VISUALIZE_PAIRS_CONNECTIONS:
        visualize_matching_pairs(pairs.copy())

    return pairs, [shift1, shift2]