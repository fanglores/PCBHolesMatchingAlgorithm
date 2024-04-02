# PCBHolesMatchingAlgorithm
An algorithm that finds matches between the holes in the drawing of the PCB and its photo upon manufacture (after drilling, which will have an error).
After that, the algorithm "stretches" the image of the original drawing over the photo of the PCB (possible to vice versa). This allows you to get an image with corrected hole positions and visually get an idea of the shifts using the included grid of lines from the original drawing.
The algorithm normalizes the points of the holes along the upper and left margins, and correlates them between the images. Then, using Delaunay triangulation, a triangular mesh is built along the points. According to the points correspondences, the grid is transferred to another image and using an Affine transformation, each triangle of the old image is transformed into a triangle of the new one.

### Program usage description
The program takes two images as inputs. The first has holes marked in blue, and the second has holes in red. The main requirement is that there is the same number of holes in each image. When the program is run, it produces a JPEG image called "output.jpeg" in the location where it was executed. This image has the same size as the second image and contains the first image stretched over the grid of the second one.

To run the program, you need to first create a virtual environment using the "venv" package in Python. Then, you can install the necessary dependencies using the "pip" command. Here is an example of how to do that:
$ pip install -r requirements.txt

This program has five modules: "Main", "Detector", "Resizer", "Helpers", and "Visualizers".
- Visualizers.py contain functions for visualizing the results, and their main purpose is to help debug a program. By using the constants DEBUG_VISUALIZE_FOUND_CONTOURS, DEBUG_VISUALIZE_RESULT_STEP_BY_STEP and others, you can turn on or off the visualization of the results at certain stages. You can close these windows by pressing the "q" key.
All the constants are explained below:
     - DEBUG_VISUALIZE_FOUND_CONTOURS (default: False): Visualizes the found contours in the images.
     - DEBUG_VISUALIZE_PAIRS_CONNECTIONS (default: False): Visualizes the mapping of holes between the images.
     - DEBUG_VISUALISE_MESHES (default: False): Visualises a constructed grid of triangles.
     - DEBUG_VISUALISED_PAIRED_MASKED_TRIANGLES_STEP_BY_STEP (default: False): Visualizes pairs of triangles from different images step by step.- DEBUG: Visualize result step by step (default: False): Visualizes the result one step at a time.
     - Debug Visualize Result (the default is false). It is recommended to use the constant below, as it will provide a more representative visualization.
     - Visualize resulting final result
     - Debug visualize with mesh (default value: false). Visualize final result with triangular mesh on topSHOULD_SAVE_RESULT: Whether to save the image with final results.
  
- Helpers.py include functions for basic calculations and image resizing within the detector module.
- Detector.py includes functions for finding centers of holes in images, aligning coordinates between two images, and normalizing. Centers are found using colored masks and contours that are determined through moments.
After coordinates are aligned, centers of holes become aligned as well. Normalization involves removing the smallest common x and y coordinates from all points within the center of each image, causing the images to fit snugly to the left and top edges of the images. This makes points in both images appear closer together when they overlap, creating a more accurate representation.A function searches for corresponding points in the second image by calculating the Euclidean distance between each pair of points and finding the closest match between the two images. Due to normalization, there is almost no chance of error in this function.
- Resizer.py includes functions for image transformations, including the transformation itself, which makes use of a triangular grid creation function and a process that transforms a triangle from the first image into a triangle in the second using the coordinates of corresponding points. Delaunay triangulation is used to create a triangular grid. Then, a mask is applied to each triangle, and it is transformed using an affine transformation, after which it is overlayed on the resulting image. Finally, all the transformed triangles are combined to create the final image, which is saved to a computer.
- Main.py implements the algorithm itself: searching for the centers, matching of coordinates, and the transformation of images.
