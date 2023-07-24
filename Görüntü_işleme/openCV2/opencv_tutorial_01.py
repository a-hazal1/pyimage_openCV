import imutils
import cv2

# giriş görüntüsünü yükleyin ve boyutlarını gösterin, bunu aklınızda bulundurun
# görüntü, çok boyutlu bir NumPy dizisi olarak temsil edilir.
# şekil numarası sıra (yükseklik) x hayır. sütunlar (genişlik) x hayır. kanallar (derinlik)
image = cv2.imread("C:\Users\Hazal\OneDrive\Masaüstü\openCV2\image.png")
(h, w, d) = image.shape
print("width={}, height={}, depth={}".format(w, h, d))

# görüntüyü ekranımıza göster -- pencereye tıklamamız gerekecek
# OpenCV ile açın ve yürütmeye devam etmek için klavyemizde bir tuşa basın
cv2.imshow("Image", image)
cv2.waitKey(0)