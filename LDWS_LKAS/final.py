import cv2
from ultralytics import YOLO
import numpy as np
import openni
from openni import openni2,_openni2
import serial
import time
#Paramters:



#Threshold for considering the drift needs to be corrected
threshold=4
#Maximum differance in position between each frame ( For smoothing )
maxstep=2
#A constant added to drift to compensate for camera placement (in pixels)
drift_correction=0
#video_path
#video_path="project_video.mp4"
#video_path="vid2.mp4"


#Kinect
openni2.initialize()  # Initialize OpenNI
dev = openni2.Device.open_any()  # Open a connection to any available device
depth_stream = dev.create_depth_stream()  # Create a depth stream
depth_stream.start()  # Start the depth stream
color_stream = dev.create_color_stream()  # Create a color stream
color_stream.start()    # Start the color stream
 #color_mode = openni.VideoMode()
 #color_mode.resolutionX = 1280
 #color_mode.resolutionY = 720      


'''              
cv2.imshow('depth', depth_uint8)
cv2.imshow('depth colored', depth_colored)
cv2.imshow('color', color)
out_img = self.forward(color) ######################
cv2.imshow("OUTPUT",out_img)        ######################
if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    '''          


                                #####mahetab#####

# Load condition images with transparency

warning_img=cv2.imread("warning.png", cv2.IMREAD_UNCHANGED)

# Resize condition images to fit the corner of the video
corner_width, corner_height = 200, 200

warning_img=cv2.resize(warning_img, (corner_width, corner_height))


#Load Video For Testing:
#clip=cv2.VideoCapture(video_path)


############
#FOR VID2:
#frame_num=70000
#clip.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
#############


# Get video properties
#height = clip.get(cv2.CAP_PROP_FRAME_HEIGHT)
#width = clip.get(cv2.CAP_PROP_FRAME_WIDTH)


#For kinect
height=480
width=640


                 #####mahetab#####
stream=True
frameid=0

               #####mahetab#####
# for image transparent
def overlay_image_alpha(img, img_overlay, x, y, alpha_mask):
    """Overlay `img_overlay` onto `img` at (x, y) with alpha channel."""
    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if no part of the image is in the range
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    # Blend overlay within the determined ranges
    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
    alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis]
    alpha_inv = 1.0 - alpha

    img_crop[:] = alpha * img_overlay_crop[:, :, :3] + alpha_inv * img_crop


#Finding center of frame ( Car Center )
center_x, center_y = (int(width/2))+drift_correction, int(height/1.2)
old_x=center_x



def determine_line_color(drift,threshold):
    if abs(drift)<=threshold:
        good_lane_keeping_y_position =corner_height + 30
        cv2.putText(frame, "Good Lane Keeping", (10, good_lane_keeping_y_position), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        return (124,250,0)#Green
    else:
            # Split the alpha channel
        b, g, r, a = cv2.split(warning_img)
        overlay_img = cv2.merge((b, g, r))
        alpha_mask = a / 255.0

        distance_value=str("%.2f" % round(abs(drift/10),2))
        overlay_image_alpha(frame, overlay_img, 0, 0,alpha_mask)
        if drift<(threshold*-1):
            rotation_message = f"Move {distance_value} m to the Left"
            rotation_message_y_position = corner_height + 30
            cv2.putText(frame, rotation_message, (10, rotation_message_y_position), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        elif drift>threshold:
            rotation_message =f"Move {distance_value} m to the Right"
            rotation_message_y_position = corner_height + 30
            cv2.putText(frame, rotation_message, (10, rotation_message_y_position), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return (20,40,244) #red
    

  
#Function to Find Lane Center :
def find_center_lane(lanes,seg):
    try:
        if seg == 0:
            #convert each box to array
            lanes=lanes.xyxy.cpu().numpy()
            centers=[]
            rightflag=0
            #Finding Center of each lane
            for lane in lanes:
                lane_x_center=(lane[0]+lane[2])/2
                lane_y_center=(lane[1]+lane[3])/2
                centers.append([lane_x_center,lane_y_center])
            #Finding the lanes closest to center
            x_distances_to_center=[]
            for lane in centers: 
                distance=lane[0]-center_x
                x_distances_to_center.append(distance)
           
            #Find the smallest 2 distances from left and right (Closest to center)
            #Initialize right to infinity, left to negative  infinity
            laneright=float('inf')
            laneleft=float('-inf')
            for element in x_distances_to_center:
                if element>0:
            # Update laneright if element is smaller
                    if element < laneright:
                        laneright=element      
        # Update laneleft if element is bigger
                if element<0:
                    if element>laneleft:
                        laneleft=element
        #Failsafe block
            if laneright==('inf'):
                laneright=x_distances_to_center[0]
            if laneleft== ('-inf'):
                laneleft=x_distances_to_center[0]
            lanes_smallest_indeces= [x_distances_to_center.index(laneright),x_distances_to_center.index(laneleft)]
            #print(lanes_smallest_indeces)
            actual_center_x = int(((centers[lanes_smallest_indeces[0]][0]+centers[lanes_smallest_indeces[1]][0]))/2)
            #print(actual_center_x)
            return(actual_center_x)
    except Exception:
        return center_x



# YOLO model initialization and prediction
model = YOLO('best.pt')


#Main Loop
while (1):
    #KINECT::::::::::::::::::
    
    #Get depth frame
    depth_frame = depth_stream.read_frame()       
    h, w = depth_frame.height, depth_frame.width

    depth = np.ctypeslib.as_array(
        depth_frame.get_buffer_as_uint16()).reshape(h, w)     # Get the depth frame data
    depth_scale_factor = 255.0 / depth_stream.get_max_pixel_value()
    depth_uint8 = cv2.convertScaleAbs(depth, alpha=depth_scale_factor)
    depth_colored = cv2.applyColorMap(depth_uint8, cv2.COLORMAP_HSV)
    #Get color
    color_frame = color_stream.read_frame()
    color = np.ctypeslib.as_array(color_frame.get_buffer_as_uint8()).reshape(h,w, 3)
    color= np.array(color)
    frame = cv2.cvtColor(color, cv2.COLOR_RGB2BGR)
    #frame= cv2.resize(color, (1280,720))
    
    ##########################################
    # Display the results
        
    #ret,frame=clip.read()
    results = model.predict(source=frame, show=False, conf=0.25, show_boxes=True)
    lanes = results[0].boxes

    #Print box coordinates
    cv2.circle(frame, (center_x, center_y), radius=15, color=(255, 0, 0), thickness=5)
    actual_center_x=find_center_lane(lanes,seg=0)
    """
        Drift : 
        -Positive : Car is drifting to the right and needs to go to the left 
        -Negative : Car is drifting to the left and Needs to go to the right
        -Scale : -50 to +50 
        -Suggested Threshold could be 1 or 2 (if 2< drift <-2 car is in lane)

    """

    #Max step parameter is used to smooth output and decrease the effect of wrong predictions
    if abs((actual_center_x - old_x))>maxstep:
        if actual_center_x>old_x:
            actual_center_x=old_x+maxstep
        if actual_center_x<old_x:
            actual_center_x=old_x-maxstep
    old_x=actual_center_x
    drift=((actual_center_x-center_x)/width)*100
    print(drift)

    #Draw circles and line to show vehicle's position in lane:
    line_color=determine_line_color(drift,threshold)
    cv2.circle(frame, (actual_center_x, center_y), radius=15, color=(255, 255, 0), thickness=5)
    cv2.line(frame,(actual_center_x,center_y),(center_x,center_y),line_color,thickness=3)
    cv2.imshow("results",results[0].plot(boxes=True))


    # Specify the COM port and baud rate
    com_port = 'COM12'  # Update this to your Arduino's COM port
    baud_rate = 9600   # Ensure this matches the Arduino's baud rate

    # Initialize the serial connection
    ser = serial.Serial(com_port, baud_rate, timeout=1)

    def send_value(value):
        # Send the value to the Arduino
        ser.write(f"{value}\n".encode())

    try:

        send_value(drift)
    except KeyboardInterrupt:
        print("Program stopped")
    finally:
        ser.close()  # Close the serial connection
    #Quitting:
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
cv2.destroyAllWindows()