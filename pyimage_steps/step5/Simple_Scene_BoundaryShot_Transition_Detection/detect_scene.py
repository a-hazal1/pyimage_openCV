import argparse
import imutils
import cv2
import os
# bağımsız değişken ayrıştırıcısını oluştur ve bağımsız değişkenleri ayrıştır
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, type=str,
	help="path to input video file")
ap.add_argument("-o", "--output", required=True, type=str,
	help="path to output directory to store frames")
ap.add_argument("-p", "--min-percent", type=float, default=1.0,
	help="lower boundary of percentage of motion")
ap.add_argument("-m", "--max-percent", type=float, default=10.0,
	help="upper boundary of percentage of motion")
ap.add_argument("-w", "--warmup", type=int, default=200,
	help="# of frames to use to build a reasonable background model")
args = vars(ap.parse_args())
# arka plan çıkarıcıyı başlat
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
# belirli bir çerçevenin olup olmadığını temsil etmek için kullanılan bir boole başlat
# iki tamsayı sayacıyla birlikte yakalandı -- biri sayılacak
# yakalanan toplam kare sayısı ve bir tane daha
# işlenen toplam kare sayısını say
captured = False
total = 0
frames = 0
# video dosyasının genişliğini ve yüksekliğini başlatmak için bir işaretçi açın
vs = cv2.VideoCapture(args["video"])
(W, H) = (None, None)

# videonun kareleri üzerinde döngü
while True:
	# videodan bir kare yakala
	(grabbed, frame) = vs.read()
	#frame Yok ise, bitir
    # video dosyası
	if frame is None:
		break
	# orijinal framei klonla (böylece daha sonra kaydedebiliriz), yeniden boyutlandırın
    # ardından arka plan çıkarıcıyı uygula
	orig = frame.copy()
	frame = imutils.resize(frame, width=600)
	mask = fgbg.apply(frame)
	# gürültüyü ortadan kaldırmak için bir dizi aşındırma ve genişleme uygula
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	# genişlik ve yükseklik boşsa, uzamsal boyutları al
	if W is None or H is None:
		(H, W) = mask.shape[:2]
	# "ön plan" olan maskenin yüzdesini hesapla
	p = (cv2.countNonZero(mask) / float(W * H)) * 100
    # "ön plan" olarak framein %N'sinden daha azı varsa, hareket durur 
	if p < args["min_percent"] and not captured and frames > args["warmup"]:
		
		cv2.imshow("Captured", frame)
		captured = True
		# çıktı çerçevesine giden yolu oluştur
        # toplam frame sayacı
		filename = "{}.png".format(total)
		path = os.path.sep.join([args["output"], filename])
		total += 1
		# *orijinal, yüksek çözünürlüklü* framei diske kaydedin
		print("[INFO] saving {}".format(path))
		cv2.imwrite(path, orig)
	# aksi halde ya sahne değişiyor ya da biz hala ısınma aşamasındayız
    # mod yani sahne düzelene veya işimiz bitene kadar bekleyelim
    # arka plan modelini oluşturma
	elif captured and p >= args["max_percent"]:
		captured = False
    
	cv2.imshow("Mask", mask)
	key = cv2.waitKey(1) & 0xFF
	
	if key == ord("q"):
		break
	# kare sayacını artır
	frames += 1

vs.release()

