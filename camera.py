#!/usr/bin/python
import cv2
import time

class Camera():
	# Constructor...
	def __init__(self):
		w     = 640			# Frame width...
		h     = 480			# Frame hight...
		fps   = 20.0                    # Frames per second...
		resolution = (w, h)         	# Frame size/resolution...
 
		self.cap = cv2.VideoCapture(0)  # Prepare the camera...
		print("Camera warming up ...")
		time.sleep(1)
		# Prepare Capture
		self.ret, self.frame = self.cap.read()
 
		# Prepare output window...
		self.winName = "Motion Indicator"
		cv2.namedWindow(self.winName, cv2.WINDOW_AUTOSIZE)
 
		# Read three images first...
		self.prev_frame     = cv2.cvtColor(self.cap.read()[1],cv2.COLOR_RGB2GRAY)
		self.current_frame  = cv2.cvtColor(self.cap.read()[1],cv2.COLOR_RGB2GRAY)
		self.next_frame	    = cv2.cvtColor(self.cap.read()[1],cv2.COLOR_RGB2GRAY)
 
		# Define the codec and create VideoWriter object
		self.fourcc = cv2.VideoWriter_fourcc(*'H264')     # You also can use (*'XVID')
		self.out = cv2.VideoWriter('output.avi',self.fourcc, fps, (w, h), True)
		
		# Capture an image for the streaming to a browser...
		s, img = self.cap.read()
		if s:	# frame captured without any errors...
			cv2.imwrite("stream.jpg", img)	# Save image...		
	
	# Frame generation for Browser streaming wiht Flask...	
	def get_frame(self):
		self.frames = open("stream.jpg", 'w+')
		s, img = self.cap.read()
		if s:	# frame captures without errors...
			cv2.imwrite("stream.jpg", img)	# Save image...
		return self.frames.read()
        
			
	def diffImg(self, tprev, tc, tnex):
		# Generate the 'difference' from the 3 captured images...
		Im1 = cv2.absdiff(tnex, tc)
		Im2 = cv2.absdiff(tc, tprev)
		return cv2.bitwise_and(Im1, Im2)
 
	def captureVideo(self):
		# Read in a new frame...
		self.ret, self.frame = self.cap.read()
		# Image manipulations come here...
                # This line displays the image resulting from calculating the difference between
                # consecutive images...
		diffe = self.diffImg(self.prev_frame, self.current_frame, self.next_frame)
		cv2.imshow(self.winName,diffe)
		
		# Put images in the right order...
		self.prev_frame		= self.current_frame
		self.current_frame	= self.next_frame
		self.next_frame		= cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
		return()
 
	def saveVideo(self):
		# Write the frame...
		self.out.write(self.frame)
		return()
 
	def __del__(self):
		self.cap.release()
		cv2.destroyAllWindows()
		self.out.release()
		print("Camera disabled and all output windows closed...")
		return()

def main():
	# Create a camera instance...
	cam1 = Camera()

	while(True):
		# Display the resulting frames...
		cam1.captureVideo()    # Live stream of video on screen...
		cam1.saveVideo()       # Save video to file 'output.avi'...
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	return()

if __name__=='__main__':
	main()
