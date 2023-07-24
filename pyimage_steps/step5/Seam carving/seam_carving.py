from skimage import transform
from skimage import filters
import argparse
import cv2
# bağımsız değişkeni oluştur, bağımsız değişkenleri ayrıştır 
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image file")
ap.add_argument("-d", "--direction", type=str,
	default="vertical", help="seam removal direction")
args = vars(ap.parse_args())

# görüntüyü yükleyin ve gri tonlamaya dönüştürün
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Sobel gradyan büyüklük temsilini hesapla
# görsel -- bu bizim "enerji haritamız" olacak
# seam carving algoritmasına gir
mag = filters.sobel(gray.astype("float"))
# orijinal resmi göster
cv2.imshow("Original", image)

# kaldırmak için bir dizi üzerinde döngü yapın
for numSeams in range(20, 140, 20):
	# dikiş oyma işlemini gerçekleştirin, istenen numarayı çıkar Resimdeki karelerin sayısı -- `dikey` kesimler
    # 'yatay' kesimler yapılırken görüntü genişliğini değiştirin
    # görüntü yüksekliğini değiştir
	carved = transform.seam_carve(image, mag, args["direction"],
		numSeams)
	print("[INFO] removing {} seams; new size: "
		"w={}, h={}".format(numSeams, carved.shape[1],
			carved.shape[0]))
	
	cv2.imshow("Carved", carved)
	cv2.waitKey(0)

