from imutils import paths
import argparse
import cv2
def variance_of_laplacian(image):
	# görüntünün Laplacian'ını hesaplayın ve ardından odağı geri getirin
    # Laplacian'ın varyansı olan ölçü   
	return cv2.Laplacian(image, cv2.CV_64F).var()
# bağımsız değişkeni oluştur, bağımsız değişkenleri ayrıştır
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=100.0,
	help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())
# giriş görüntüleri üzerinde döngü
for imagePath in paths.list_images(args["images"]):
	# görüntüyü yükleyin, gri tonlamaya dönüştürün ve
    # Laplacian Varyansını kullanarak görüntünün odak ölçüsü
    # yöntem
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = variance_of_laplacian(gray)
	text = "Not Blurry"
	# odak ölçüsü sağlanan eşiğin altındaysa o zaman görüntü "bulanık" olarak kabul edilmelidir
	if fm < args["threshold"]:
		text = "Blurry"
	
	cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
		cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
	cv2.imshow("Image", image)
	key = cv2.waitKey(0)