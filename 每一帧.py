import os
 
import cv2
import cv
 
videos_src_path = 'E:\\liufangtao\\hat\\helmet\\'
videos_save_path = 'E:\\liufangtao\\hat\\helmet\\1\\'
 
videos = os.listdir(videos_src_path)
videos = filter(lambda x: x.endswith('mp4'), videos)


 
for each_video in videos:
	print(each_video)
	each_video_name, _ = each_video.split('.')
	# print(each_video_name)
	each_video_full_path = os.path.join(videos_src_path, each_video)
	cap = cv2.VideoCapture(each_video_full_path)

	c = 0
	timeF = 100000

	frame_count = 1
	success = True
	while(success):
		success, frame = cap.read()
		print('Read a new frame: ', success)
		if (c % timeF == 0):
		# params = []
		# params.append(cv.CV_IMWRITE_PXM_BINARY)
		# params.append(1)
		    cv2.imwrite(videos_save_path + each_video_name + "_%d.jpg" % int(c/100000), frame,[int( cv2.IMWRITE_JPEG_QUALITY), 95])
		    frame_count = frame_count + 1
		c = c + 10000
	cap.release()

	# # get the name of each video, and make the directory to save frames
    
    # os.mkdir(videos_save_path + '/' + each_video_name) 
    
 
    # each_video_save_full_path = os.path.join(videos_save_path, each_video_name) + '.jpg'
 
    # get the full path of each video, which will open the video tp extract frames
    
 
    
    
   
    
    	
    	
 
        
        
        
        
 
        
    