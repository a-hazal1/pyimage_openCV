from imutils import build_montages
from imutils import paths
import argparse
import random
import cv2

# bağımsız değişkeni oluştur, bağımsız değişkenleri ayrıştır
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
ap.add_argument("-s", "--sample", type=int, default=21,
	help="# of images to sample")
args = vars(ap.parse_args())

# görüntülere giden yolları yakalayın, ardından rastgele bir örnek seç
imagePaths = list(paths.list_images(args["images"]))
random.shuffle(imagePaths)
imagePaths = imagePaths[:args["sample"]]

# resim listesini başlat
images = []
# görüntü yolları listesi üzerinde döngü
for imagePath in imagePaths:
	# görüntüyü yükleyin ve görüntü listesini güncelleyin
	image = cv2.imread(imagePath)
	images.append(image)
# görüntüler için montajlar oluşturun
montages = build_montages(images, (128, 196), (5, 3))
for montage in montages:
	cv2.imshow("Montage", montage)
	cv2.waitKey(0)
