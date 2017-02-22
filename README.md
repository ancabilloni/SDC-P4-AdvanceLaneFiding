# Advanced Lane Finding
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

The scope for this project is to find detect lane on a given recorded driving track. This is the 4th project in Term 1 Udacity Self Driving Car nanodegree. Recorded video and many referenced sample codes are provided by Udacity

## Installation & Resources
1. Anaconda Python 3.5
2. Udacity [Carnd-term1 starter kit](https://github.com/udacity/CarND-Term1-Starter-Kit) with miniconda installation 
3. Udacity [provided data](https://github.com/udacity/CarND-Advanced-Lane-Lines)

## Files
`find_lanes.ipynb` : jupyter notebook with all codes and demonstration.

## Goals
1. Calculate camera calibration and provide example of distortion corrected calibration image. Calibrate and correct distortion on test images. Provide example.
2. Describe and apply gradients transform on image. Provide example.
3. Describe and apply perspective transform of image. Provide example.
4. Describe how to find lane-line pixels and fit their position in an polynomial. Provide example.
5. Describe how to calculate radius of curvature of the lane and the position of vehicle with respect to center.
6. Provide an example of image after all of the above applied into an image.
7. Provide a video result after all the above applied to every frame of the given project video.
8. End discussion

## I. Calibration
Photo taken by camera tends to have some type of distortion in it. There are two type of distortions: radial distortion (straight line appears curve) and tangential distortion (some area of an image looks nearer than expect). (*Source*: [OpenCV](http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_calib3d/py_calibration/py_calibration.html)). Distortion produces incorrect presentation of real scene for implementation such as Lane Dectection. To fix this, undistortion procedure can be applied by calibration

To undistort an image, we need to know the distortion coefficients and camera matrix:
- First, I create a list of object points with shape `(nx*ny,3)` represent `(x,y,z)` coordinates. Assume z is 0 because chessboard is stationary, so x & y are the only coordinates that move.
- Second, I apply `cv2.findChessboardCorners(gray,(nx,ny),None)` function in a series of provided chessboard images. This steps will help to find a set of defined corners nx by ny corners within the chessboard.
  - If found, the defined corners coordinates will be added into a `imgpoints` (2D points) list and object points in step 1 will be also added into a `objpoints` (3D points) list.
- Third, I apply `cv2.calibrateCamera(objpoints,imgpoints,grayimage.shape[::-1],None,None)` to find the camera matrix `mtx` and distortion coeffcients `dist` from `objpoints` and `imgpoints` information.
- Lastly, to undistort image `img`, I apply `cv2.undistort(img,mtx,dist,None,mtx)`.

Find codes in `Calibration` and `Help Codes`.

Below is an example on one of the chessboard images. Left is original image and Right is the undistorted image.

*Comment*: In the example below, (nx,ny) = (9,6) which represents 9 possible corners in each of 6 rows. The images show improvement that some curve lines in original image change into straight line after undistortion.

![chessboard_undistort](https://cloud.githubusercontent.com/assets/23693651/22965319/045eeb82-f32b-11e6-82fe-b5fa407eb9d1.png)

Another example from one of the test image. As they aren't obvious to see the differences right away like the chessboard, some color boxes are provided to point out the differences. Since the curves of image were being straighten, some of the features such as part of the car and the tree on left and right sides were pushing out of the image original dimension.

![raw_indist](https://cloud.githubusercontent.com/assets/23693651/22965408/73205f1a-f32b-11e6-869d-d4c0972e7c88.png)

## II. Binary Threshold
The next important task of finding lane lines is to convert color image into binary. With only black and white pixel in binary image, it's easier to detect the lane pixels.
For this project, I choose to combine gradient threshold on X direction `OR` S channel threshold (from HLS) `AND` V channel threshold (from HSV). I also apply a mask to the binary image to keep only the interest area and remove the rest to reduce noise.
Find codes in `Help Codes`.

Below is an example of Original -> Binary Image -> Masked Image

![binary_threshold](https://cloud.githubusercontent.com/assets/23693651/23200884/defc0698-f8a4-11e6-8493-5b5a3a8970f4.png)

## III. Transformation - Bird Eye View
After finding binary image with region of interest, a transformation is needed to see the lane like from the top down or in bird-eye view. It is more accurate to use bird-eye view for any curvature calculation because the view plane faces parallel to the ground. To do so, I applied `cv2.getPerspectiveTransform(src,dst)` to find a perspective transform matrix from source coordinate `src` and transform to destination `dst`. `src` and `dst` are referenced from Udacity's write up example. Find codes in `Help Codes`.

![birdeye](https://cloud.githubusercontent.com/assets/23693651/23200885/e0a09be4-f8a4-11e6-9223-5f6239f57902.png)

## IV. Lane Lines Polynomial
The method to find lane lines polynomial is: 

1. Use histogram plot to find the highest peak locations of white pixels in binary image.
2. Then apply sliding windows to find average locations make up the line curvatures.
3. Find all the white pixels of left and right lines.
4. Apply `numpy.polyfit()` to find the polynomial coeffcients that make the poly equation best fit into the curvature coordinates of left and right lines. For this project, we will find coeffients of 2nd polynomial because the curves are not complicated to use any higher polynominal order function.

For next frame, histogram can be skipped by using the last known location of the lines from the previous frame. To make sure the lines are smooth, global variables are applied to find average polynominal coefficients of latest 5 frames to apply to the most current frame.

Find codes in `Pipeline`.

## V. Curvature Radius and Offcenter
Curvature radius is defined by equation `R = [(1+(2*A*y)^2)^(3/2)]/|2*A|` while `f(y) = A*y^2 + B*y + C`. [A,B,C] is calculated by `np.polyfit()` and `y` value is the maximum `y` coordinate which is the bottom of the image. Since there are 2 lanes, 2 radius curvatures can be calculated. The final radius curvature is the average of two radius Left and Right.

Assume the camera is mounted in the center of the car, so the center of the image is the center position of the car. To find how far the car is off lane center: 
Finding the center between the two poly lines in pixels -> Find the difference of image center and center between poly lines -> Convert from pixel to meter -> This is the offset of the car to center of the lane.

Meter to pixel ratios are: y_direction = 30/720, x_direction = 3.7/700. These values approximation that the width of the lane is 3.7 meter and the length of the lane in the image is 30 meters, provided by Udacity. 

Find functions in `Help Codes`

## VI. Apply all of above (Pipeline) into a test image
Here is a result after applying all steps as mentioned above into a test image:

![test_lanes](https://cloud.githubusercontent.com/assets/23693651/23200890/e373364c-f8a4-11e6-886a-84dcdca550a8.png)

## VII. Apply Pipeline into a test video
Here is the video showing the result of lane detection using steps describe above

![Project Video](https://youtu.be/wXhlNZUeyuE)

## VIII. End Discussion
The main challenge here is to define a appropriate threshold combination for the binary image since there are a number of varibales such as random lighting, shadows, lane line colors, road colors,etc..
Future works:
As the code are being built based on basic functions, I think I can better improve the structure with more object oriented coding by using `class`.
There are couple more challenge videos with more tricky environment provided, so I will test to see the robustness of the detection and try on different ways to make it more robust to adapt with other environment as well.
