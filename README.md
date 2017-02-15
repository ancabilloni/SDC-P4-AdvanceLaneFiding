# Advanced Lane Finding
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

The scope of this project is to....

## Installation & Resources
1. Anaconda Python 3.5
2. Udacity [Carnd-term1 starter kit](https://github.com/udacity/CarND-Term1-Starter-Kit) with miniconda installation 
3. Udacity [provided data](https://github.com/udacity/CarND-Advanced-Lane-Lines)

## Files and Usage
`find_lanes.ipynb` : jupyter notebook with all codes and demonstration.

## Goals
1.
2.
3.
4.
5.
6.
7.
8.
9.

## I. Calibration
Intro:
To calibrate:
- First, I create a list of object points with shape `(nx*ny,3)` represents `(x,y,z)` coordinates. Assume z is 0 because chessboard is stationary, so x & y are the only coordinates that move.
- Second, I apply `cv2.findChessboardCorners(gray,(nx,ny),None)` function in a series of provided chessboard images. This steps will help to find a set of defined corners nx by ny corners within the chessboard.
  - If found, the defined corners coordinates will be added into a `imgpoints` (2D points) list and object points in step 1 will be also added into a `objpoints` (3D points) list.
- Third, I apply `cv2.calibrateCamera(objpoints,imgpoints,grayimage.shape[::-1],None,None)` to find the camera matrix `mtx` and distortion coeffcients `dist`.
- Lastly, to undistort image `img`, I apply `cv2.undistort(img,mtx,dist,None,mtx)`.
Below is an example on one of the chessboard images. Left is original image and Right is the undistorted image.

*Note*: In the example below, (nx,ny) = (9,6) which represents 9 possible corners in each of 6 rows.
![chessboard_undistort](https://cloud.githubusercontent.com/assets/23693651/22965319/045eeb82-f32b-11e6-82fe-b5fa407eb9d1.png)

Another example from one of the test frame from actual video. As they aren't obvious to see the differences right away like the chessboard, some color boxes are provided to point out the differences.
![raw_indist](https://cloud.githubusercontent.com/assets/23693651/22965408/73205f1a-f32b-11e6-869d-d4c0972e7c88.png)

## II. Binary Threshold
The next important task of finding lane lines is to convert color image into binary. With only black and white pixel in binary image, it's easier to detect the lane pixels.
For this project, I choose to combine gradient threshold on X direction OR s channel threshold AND v channel threshold. I also apply a mask to the binary image to only keep the interest area and discard the rest.

Below is an example of Original -> Binary Image -> Masked Image

![binary_threshold](https://cloud.githubusercontent.com/assets/23693651/22967152/4eb8620a-f333-11e6-8e92-54c1f0ce8f8e.png)

## III. Transformation - Bird Eye View
After finding binary image with region of interest, a transformation is need to see the lane like from the top down or we call it bird-eye view. To do so, I applied `cv2.getPerspectiveTransform(src,dst)` to find a perspective transform matrix from source coordinate `src` and transform to destination `dst`

![birdeye](https://cloud.githubusercontent.com/assets/23693651/22967624/37251aaa-f335-11e6-86a1-978da153cd36.png)


