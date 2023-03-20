# winter-assignment
VideoFy- This is my submission for Winter Assignment 2023 (Individual 1Y).

About - Using my application you can watch videos/movies with your friend (without going to his room) without spending alot of internet data and device storage (provided both of you are on the same local network). Not only this both of you can also control the video like (forward rewind play pause etc.) 

Features:

Users can watch video without spending their storage and internet data.
Users can control the video by pressing the following keys on keyboard:
r = rewind video by 10 secs
f = forward video by 10 secs 
p = play/pause the video
q = quit the video

How to start? Clone the repository to your local system using git clone. Run the terminal in that folder and install all necessary packages.
You have to enter name of video in the 13th line of code(filename = "enter name") in server1.py file and keep the video file and code file in the same folder. Type 'python3 server1.py' in terminal and run it. Then type 'python3 client1.py' in terminal and run it. 

Tech Stack 
socket programming in python - to establish communication between client and server.
cv2 = to display video
imutils = to process video frames
pyaudio = to play video with audio
pickle = to convert objects to bytes

Workflow of my application
I created three sockets:
1. For video transmission 
2. For audio transmission 
3. For message transmission
video part - I used the cv2 module to read the frames, then I encoded them and sent them to the client. 
audio part - I used the cv2 module to process the sound file, then I encoded it and sent them to the client. 
message part - I used the waitkey() function of cv2 module. This function waits for a very small time after every frame for a key to be pressed.If a particular key is pressed it executes the code defined for it. In my case I made the client send a message to the server on pressing the key. On the server side I put the if condition i.e if message = "particular mention" execute the code(logics behind various controls)

Author Somya Chawla

License Licensed under the MIT License
