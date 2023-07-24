from imutils.video import VideoStream
import imutils
import time
import cv2
# hareket belirginliği nesnesini başlat ve video akışını başlat
saliency = None
vs = VideoStream(src=0).start()
time.sleep(2.0)
# loop over frames from the video file stream
while True:
	# zincirli video akışından çerçeveyi alın ve yeniden boyutlandırın
    # 500px (işlemeyi hızlandırmak için)
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	# belirginlik nesnemiz Yok ise, onu başlatmamız gerekir
	if saliency is None:
		saliency = cv2.saliency.MotionSaliencyBinWangApr2014_create()
		saliency.setImagesize(frame.shape[1], frame.shape[0])
		saliency.init()
    # giriş çerçevesini gri tonlamaya dönüştürün ve belirginliği hesaplayın
    # hareket modeline dayalı harita
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	(success, saliencyMap) = saliency.computeSaliency(gray)
	saliencyMap = (saliencyMap * 255).astype("uint8")
	
	cv2.imshow("Frame", frame)
	cv2.imshow("Map", saliencyMap)
	key = cv2.waitKey(1) & 0xFF
 
	
	if key == ord("q"):
		break

cv2.destroyAllWindows()
vs.stop()



