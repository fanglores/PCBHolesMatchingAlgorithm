import cv2
from detector import find_holes_coordinates_on_image, match_coordinates
from resizer import transform_image

try:
    img1_path = input('Image 1 path (blue mask): ')
    crd1 = find_holes_coordinates_on_image(img1_path, 'blue')

    img2_path = input('Image 2 path (red mask): ')
    crd2 = find_holes_coordinates_on_image(img2_path, 'red')

    paired_crds, shifts = match_coordinates(crd1.copy(), crd2.copy())

    result_image = transform_image(img1_path, paired_crds)
except AssertionError as e:
    print(e)
except Exception as e:
    print(f'Unknown error. Traceback:\n{e}')

cv2.destroyAllWindows()