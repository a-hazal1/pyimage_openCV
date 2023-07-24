from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
# tanımlayabilmemiz için basamak bölümleri sözlüğünü tanımlayın
# her basamak
DIGITS_LOOKUP = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 1, 0): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9
}

image = cv2.imread("C:\\Users\\Hazal\\OneDrive\\Masaüstü\\openCV_pyimage\\step5\\reconizing_digits\\images.jpg")
# görüntüyü yeniden boyutlandırarak, dönüştürerek önceden işleyin
# gri tonlama, bulanıklaştırma ve bir kenar haritası hesaplama
image = imutils.resize(image, height=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 50, 200, 255)
# kenar haritasında konturları bulun, ardından bunları özelliklerine göre sıralayın
# azalan sırada boyut
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None
# konturlar üzerinde döngü
for c in cnts:
	# kontura yaklaş
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	# konturun dört köşesi varsa, o zaman bul
	if len(approx) == 4:
		displayCnt = approx
		break
# termostat görüntüsünü çıkarın, bir perspektif dönüşümü uygulayın
warped = four_point_transform(gray, displayCnt.reshape(4, 2))
output = four_point_transform(image, displayCnt.reshape(4, 2))

# çarpık görüntüyü eşikleyin, ardından bir dizi morfolojik uygulayın
#Eşiklenmiş görüntüyü temizlemek için işlem
thresh = cv2.threshold(warped, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# eşikli görüntüde konturları bulun, ardından
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
digitCnts = []
# rakam alanı adayları üzerinde döngü
for c in cnts:
	# konturun sınırlayıcı kutusunu hesapla
	(x, y, w, h) = cv2.boundingRect(c)
	# kontur yeterince büyük bir rakam olmalıdır
	if w >= 15 and (h >= 30 and h <= 40):
		digitCnts.append(c)
# konturları soldan sağa sırala
digitCnts = contours.sort_contours(digitCnts,
	method="left-to-right")[0]
digits = []

# basamakların her biri üzerinde döngü
for c in digitCnts:
	# ROI rakamını çıkarın
	(x, y, w, h) = cv2.boundingRect(c)
	roi = thresh[y:y + h, x:x + w]
	# 7 parçanın her birinin genişliğini ve yüksekliğini hesapla
	(roiH, roiW) = roi.shape
	(dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
	dHC = int(roiH * 0.05)
	# 7 segment kümesini tanımla
	segments = [
		((0, 0), (w, dH)),	#top
		((0, 0), (dW, h // 2)),	# top-left
		((w - dW, 0), (w, h // 2)),	# top-right
		((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # center
		((0, h // 2), (dW, h)),	# bottom-left
		((w - dW, h // 2), (w, h)),	# bottom-right
		((0, h - dH), (w, h))	# bottom
	]
	on = [0] * len(segments)
    # segmentler üzerinde döngü
	for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
    # eşikli piksel ve ardından hesaplama
		segROI = roi[yA:yB, xA:xB]
		total = cv2.countNonZero(segROI)
		area = (xB - xA) * (yB - yA)
		# sıfır olmayan piksellerin toplam sayısı şundan büyükse
        # Alanın %50'si, segmenti "açık" olarak işaretleyin
		if total / float(area) > 0.5:
			on[i]= 1
	# basamağı ara ve resmin üzerine çiz
	digit = DIGITS_LOOKUP[tuple(on)]
	digits.append(digit)
	cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)
	cv2.putText(output, str(digit), (x - 10, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    
print(u"{}{}.{} \u00b0C".format(*digits))
cv2.imshow("Input", image)
cv2.imshow("Output", output)
cv2.waitKey(0)