import argparse
import imutils
import cv2
# bağımsız değişkeni oluştur, bağımsız değişkenleri ayrıştır
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())
# videoyu yükle
camera = cv2.VideoCapture(args["video"])
# döngüye devam et
while True:
	# mevcut frami al ve durum metnini başlat
	(grabbed, frame) = camera.read()
	status = "No Targets"
	# yolun sonuna gelip gelmediğimizi kontrol et
	if not grabbed:
		break
	# çerçeveyi gri tonlamaya dönüştürün, bulanıklaştırın ve kenarları algılayın
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (7, 7), 0)
	edged = cv2.Canny(blurred, 50, 150)
	# find contours 
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
    # konturlar üzerinde döngü
	for c in cnts:
		# kontura yaklaş
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.01 * peri, True)
		# yaklaşık konturun dikdörtgen olduğundan emin ol
		if len(approx) >= 4 and len(approx) <= 6:
			# yaklaşık konturun sınırlayıcı kutusunu hesapla ve
            # en boy oranını hesaplamak için sınırlayıcı kutuyu kullan
			(x, y, w, h) = cv2.boundingRect(approx)
			aspectRatio = w / float(h)
			# compute the solidity of the original contour
			area = cv2.contourArea(c)
			hullArea = cv2.contourArea(cv2.convexHull(c))
			solidity = area / float(hullArea)
			# genişlik ve yükseklik, sağlamlık ve konturun en boy oranı uygun sınırlar içinde 
			keepDims = w > 25 and h > 25
			keepSolidity = solidity > 0.9
			keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2
			# konturun tüm testlerimizi geçmesini sağlayın
			if keepDims and keepSolidity and keepAspectRatio:
				# hedefin çevresine bir taslak çizin ve durumu güncelleyin
				cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
				status = "Target(s) Acquired"
				# kontur bölgesinin merkezini hesapla
				M = cv2.moments(approx)
				(cX, cY) = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))
				(startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
				(startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
				cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
				cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)
    # durum metnini frame e yaz
	cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
		(0, 0, 255), 2)
	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	
	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()