from scipy.spatial import Delaunay
from helpers import *
from visualizators import *

TAG = '[RESIZER]'

def generate_triangular_mesh(vertexes: list):
    try:
        np_points = np.array(vertexes)
        mesh = Delaunay(np_points)
        mesh_vertexes = np.array(mesh.points[mesh.simplices], dtype=np.float32)
    except Exception as e:
        assert False, f'{TAG} Error: error while building triangular mesh.\nTraceback: {e}'

    if DEBUG_VISUALIZE_MESHES:
        visualize_triangular_mesh(mesh_vertexes)

    return mesh_vertexes

def transform_image(img_name: str, paired_coordinates: list):
    mesh_vertexes1 = generate_triangular_mesh(paired_coordinates[0])

    try:
        mesh_vertexes_pairs = get_triangles_pairs(paired_coordinates, mesh_vertexes1)
    except Exception as e:
        assert False, f'{TAG} Error: error while matching triangles.\nTraceback: {e}'

    image_src = cv2.imread(img_name)
    image_dst = cv2.imread(DST_IMG_NAME)
    result_image = np.zeros(image_dst.shape, dtype=np.uint8)

    try:
        for i in range(len(mesh_vertexes_pairs[0])):
            # Create triangle mask
            mask = np.zeros(image_src.shape[:2], dtype=np.uint8)
            cv2.fillConvexPoly(mask, np.array(mesh_vertexes_pairs[0][i]).astype(np.int32), 255)

            if DEBUG_VISUALIZE_PAIRED_MASKED_TRIANGLES_STEP_BY_STEP:
                dbgmask = np.zeros(image_src.shape[:2], dtype=np.uint8)
                cv2.fillConvexPoly(dbgmask, np.array(mesh_vertexes_pairs[1][i]).astype(np.int32), 255)

                visualize_matching_triangles(paired_coordinates, mask, dbgmask)

            # Crop only inside triangle area
            image_src_blacked = cv2.bitwise_and(image_src, image_src, mask=mask)

            # Apply Affine transformation
            matrix = cv2.getAffineTransform(mesh_vertexes_pairs[0][i], mesh_vertexes_pairs[1][i])
            warped_image = cv2.warpAffine(image_src_blacked, matrix, image_dst.shape[:2][::-1])

            # Add obtained image to result
            result_image = cv2.add(result_image, warped_image)

            if DEBUG_VISUALIZE_RESULT_STEP_BY_STEP:
                debug_show(result_image)
    except Exception as e:
        assert False, f'{TAG} Error: error while applying transformation to the image. Iteration: {i}\nTraceback: {e}'

    if DEBUG_VISUALIZE_RESULT:
        debug_show(result_image)

    if DEBUG_VISUALIZE_RESULT_WITH_MESH:
        visualize_result_with_mesh(result_image, mesh_vertexes_pairs[1])

    if SHOULD_SAVE_RESULT:
        cv2.imwrite(OUTPUT_IMAGE_NAME, result_image)

    return result_image