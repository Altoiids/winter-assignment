

import cv2, imutils, socket
import numpy as np
import time
import base64
import threading, wave, pyaudio,pickle,struct
import sys
import queue
import os


filename =  'WhatsApp Video 2023-03-07 at 1.13.50 AM.mp4'
command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(filename,'temp.wav')
os.system(command)

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
v_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 9688
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)
vid = cv2.VideoCapture("WhatsApp Video 2023-03-09 at 10.50.57 PM.mp4")
FPS = vid.get(cv2.CAP_PROP_FPS)
global TS
TS = (0.5/FPS)
BREAK=False
print('FPS:',FPS,TS)
totalNoFrames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
q = queue.Queue(maxsize=10)

durationInSeconds = float(totalNoFrames) / float(FPS)

client_message=""

def video_stream_gen():
    WIDTH=400
    while(vid.isOpened()):
        try:
            
            ret,frame = vid.read()
            frame = imutils.resize(frame,width=WIDTH)
            q.put(frame)
        except:
            os._exit(1)
    print('Player closed')
    BREAK=True
    vid.release()
	

def video_stream():
    global TS
    fps,st,frames_to_count,cnt = (0,0,1,0)
    cv2.namedWindow('TRANSMITTING VIDEO')        
    cv2.moveWindow('TRANSMITTING VIDEO', 10,30) 
    while True:
        msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ',client_addr)
        WIDTH=400
        
        while(True):
            
            frame = q.get()
            encoded,buffer = cv2.imencode('.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
            message = base64.b64encode(buffer)
            server_socket.sendto(message,client_addr)
            frame = cv2.putText(frame,'FPS: '+str(round(fps,1)),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
           
            if cnt == frames_to_count:
                try:
                    fps = (frames_to_count/(time.time()-st))
                    st=time.time()
                    cnt=0
                    if fps>FPS:
                        TS+=0.001
                    elif fps<FPS:
                        TS-=0.001
                    else:
                        pass
                except:
                    pass
            cnt+=1
            
            
           
            cv2.imshow('TRANSMITTING VIDEO', frame)

            key = cv2.waitKey(int(1000*TS)) & 0xFF	
            if key == ord('q'):
                print("check quit")
                os._exit(1)
                TS=False
                break
            global client_message	           
            if client_message == "rewind":
                print("check rewind")
                client_message=""
                ct = vid.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                print(ct)
                starting_frame = int(FPS*(ct-10))
                vid.set(cv2.CAP_PROP_POS_FRAMES, starting_frame)      
             
            if client_message == "forward":
                print("check forward")
                client_message=""
                ct = vid.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                print(ct)
                starting_frame = int(FPS*(ct+10))
                vid.set(cv2.CAP_PROP_POS_FRAMES, starting_frame)    
            
            if client_message == "play":
                print("check play")
                client_message=""
                cv2.waitKey(-1)

            if key == ord('r'):
                print("check rewind")
                client_message=""
                ct = vid.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                print(ct)
                starting_frame = int(FPS*(ct-10))
                vid.set(cv2.CAP_PROP_POS_FRAMES, starting_frame)      
             
            if key == ord('f'):
                print("check forward")
                client_message=""
                ct = vid.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                print(ct)
                starting_frame = int(FPS*(ct+10))
                vid.set(cv2.CAP_PROP_POS_FRAMES, starting_frame)    
            
            if key == ord('p'):
                print("check play")
                client_message=""
                cv2.waitKey(-1)    
            
def audio_stream():
    s = socket.socket()
    s.bind((host_ip, (port-1)))

    s.listen(5)
    CHUNK = 1024
    wf = wave.open("temp.wav", 'rb')
    p = pyaudio.PyAudio()
    print('server listening at',(host_ip, (port-1)))
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

    client_socket,addr = s.accept()

    while True:
        if client_socket:
            while True:
                data = wf.readframes(CHUNK)
                a = pickle.dumps(data)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
                print("lets check")


def msg_stream():
    v_address = (host_ip,9595)
    v_socket.bind(v_address)
    v_socket.listen()

def msg_receive():
    while True:
        ms_socket,address=v_socket.accept()
        while True:
             mess=ms_socket.recv(1024).decode()
             if mess:
                 global client_message
                 client_message=mess
                 
                 
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.submit(audio_stream)
    executor.submit(video_stream_gen)
    executor.submit(video_stream)
    executor.submit(msg_stream)
    executor.submit(msg_receive)
