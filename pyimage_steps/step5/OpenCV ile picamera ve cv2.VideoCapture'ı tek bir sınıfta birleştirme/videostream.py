from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2
# bağımsız değişkeni oluştur, bağımsız değişkenleri ayrıştır 
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
# video akışını başlatın ve kamera sensörünü kullan
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)
# video akışından kareler üzerinde döngü
while True:
	# video akışından çerçeveyi al ve yeniden boyutlandır
    # maksimum 400 piksel genişlik
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	timestamp = datetime.datetime.now()
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)
	# framei göster
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	
	if key == ord("q"):
		break

cv2.destroyAllWindows()
vs.stop()