import cv2

class Image(object):
  def __init__(self,image):
    self.image = image
    self.gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    
    
class UTW(Image):
  def __init__(self,image,object_points,image_points,src,dst,vertices):
    Image.__init__(self,image)
    self.objpoints = object_points
    self.imgpoints = image_points
    self.src = src
    self.dst = dst
  
  def region_of_interest(self):
    mask = np.zeros_like(self.image)   
    if len(mask.shape) > 2:
        channel_count = mask.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255   
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    self.masked_image = cv2.bitwise_and(self.image, mask)

  def undistort(self):
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints,self.imgpoints,gray.shape[::-1],None,None)
    self.undist = cv2.undistort(image,mtx,dist,None,mtx)

  def perspective(self):
  	M = cv2.getPerspectiveTransform(self.src,self.dst)
  	self.perspective = cv2.warpPerspective(self.undist,M,(1280,720))

  def warped(self):


