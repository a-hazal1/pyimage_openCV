import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the image file")
args = vars(ap.parse_args())

# load the image from disk and display the width, height,
# and depth
image = cv2.imread(args["image"])
(h, w, d) = image.shape
print("w: {}, h: {}, d: {}".format(w, h, d))

# show the image
cv2.imshow("Image", image)
cv2.waitKey(0)