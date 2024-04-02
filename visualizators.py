import cv2
import numpy as np

# Debug mode constants
DEBUG_VISUALIZE_FOUND_CONTOURS = False
DEBUG_VISUALIZE_PAIRS_CONNECTIONS = False
DEBUG_VISUALIZE_MESHES = False
DEBUG_VISUALIZE_PAIRED_MASKED_TRIANGLES_STEP_BY_STEP = False
DEBUG_VISUALIZE_RESULT_STEP_BY_STEP = False
DEBUG_VISUALIZE_RESULT = False
DEBUG_VISUALIZE_RESULT_WITH_MESH = False
SHOULD_SAVE_RESULT = True
OUTPUT_IMAGE_NAME = 'output.jpeg'

DEBUG_MODE = DEBUG_VISUALIZE_FOUND_CONTOURS and DEBUG_VISUALIZE_PAIRS_CONNECTIONS and DEBUG_VISUALIZE_MESHES and DEBUG_VISUALIZE_PAIRED_MASKED_TRIANGLES_STEP_BY_STEP and DEBUG_VISUALIZE_RESULT_STEP_BY_STEP and DEBUG_VISUALIZE_RESULT and DEBUG_VISUALIZE_RESULT_WITH_MESH

if DEBUG_MODE:
    DEBUG_WINDOW_NAME = "Debug Window"
    cv2.namedWindow(DEBUG_WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(DEBUG_WINDOW_NAME, 1518//2, 1090//2)

def debug_show(img):
    if DEBUG_MODE:
        q = -1
        while q != ord('q'):
            cv2.imshow(DEBUG_WINDOW_NAME, img)
            q = cv2.waitKey(250)

def visualize_contours(in_image, contours, centers):
    image = in_image.copy()

    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

    for p in centers:
        cv2.circle(image, p, 3, (0, 255, 255), -1)

    debug_show(image)

def visualize_matching_pairs(pairs: list):
    width = max([p[0] for p in pairs[0]] + [p[0] for p in pairs[1]]) + 30
    height = max([p[1] for p in pairs[0]] + [p[1] for p in pairs[1]]) + 30

    blank_image = np.zeros((height, width, 3), np.uint8)

    for i in range(len(pairs[0])):
        cv2.circle(blank_image, pairs[0][i], 5, (255, 0, 0), -1)
        cv2.circle(blank_image, pairs[1][i], 5, (0, 0, 255), -1)
        cv2.line(blank_image, pairs[0][i], pairs[1][i], (0, 255, 255), 2, 8)

    debug_show(blank_image)

crutch_counter = 1
def visualize_triangular_mesh(triangles: list):
    global crutch_counter
    image = cv2.imread(f'photo_{crutch_counter}.tif')
    crutch_counter += 1

    for tri in triangles:
        p1, p2, p3 = np.array(tri[0], dtype=int), np.array(tri[1], dtype=int), np.array(tri[2], dtype=int)
        cv2.circle(image, p1, 8, (0, 255, 0), -1)
        cv2.circle(image, p2, 8, (0, 255, 0), -1)
        cv2.circle(image, p3, 8, (0, 255, 0), -1)
        cv2.line(image, p1, p2, (0, 255, 255), 2, 8)
        cv2.line(image, p1, p3, (0, 255, 255), 2, 8)
        cv2.line(image, p2, p3, (0, 255, 255), 2, 8)

    debug_show(image)

def visualize_matching_triangles(pairs: list, mask1, mask2):
    blank_image = cv2.merge((mask1, cv2.bitwise_and(mask1, mask2), mask2))

    for i in range(len(pairs[0])):
        cv2.circle(blank_image, pairs[0][i], 5, (255, 0, 0), -1)
        cv2.circle(blank_image, pairs[1][i], 5, (0, 0, 255), -1)
        cv2.line(blank_image, pairs[0][i], pairs[1][i], (0, 255, 255), 2, 8)

    debug_show(blank_image)

def visualize_result_with_mesh(result_image, mesh_vertexes: list):
    image = result_image.copy()

    for tri in mesh_vertexes:
        p1, p2, p3 = np.array(tri[0], dtype=int), np.array(tri[1], dtype=int), np.array(tri[2], dtype=int)
        cv2.circle(image, p1, 4, (0, 255, 0), -1)
        cv2.circle(image, p2, 4, (0, 255, 0), -1)
        cv2.circle(image, p3, 4, (0, 255, 0), -1)
        cv2.line(image, p1, p2, (0, 255, 255), 1, 8)
        cv2.line(image, p1, p3, (0, 255, 255), 1, 8)
        cv2.line(image, p2, p3, (0, 255, 255), 1, 8)

    debug_show(image)