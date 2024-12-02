
# from pyzbar import pyzbar
# from pyzbar.pyzbar import decode
# from pydub import AudioSegment
# from pydub.playback import play
# import cv2

# cap=cv2.VideoCapture(0)
# cap.set(3,640)
# cap.set(4,480)

# camera =True
# while camera ==True:
#     success,frame =cap.read()
#     for code in decode(frame):
#         print(code.type)
#         print(code.data)
#     cv2.imshow('testing',frame)
#     cv2.waitKey(1)
# # # song = AudioSegment.from_wav('beep-02.wav')
# # while cap.isOpened():
# #     success,frame = cap.read()
# #     # flip the image like mirro
# #     frame =cv2.flip(frame,1)
# #     # detect barcode
# #     detectedBarCode = decode(frame,)
    
# #     if not detectedBarCode:
# #         print('no barcode')
# #     else:
# #         for barcode in detectedBarCode:
# #             # if barcode id blank
# #             if barcode.data !='':
# #                 cv2.putText(frame,str(barcode.data),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,255),2)
# #                 cv2.imwrite('code.png',frame)
# #                 # play(song)
# #                 print(barcode.data)
# #                 break

# #     cv2.imshow('scanner',frame)
# #     if cv2.waitKey(1)==ord('q'):
# #         break


# from tabulate import tabulate
 
# t=tabulate([['Aditi', 19], ['Anmol', 16], 
#                 ['Bhavya', 19], ['Ananya', 19], 
#                 ['Rajeev', 50], ['Parul', 45]],
#                headers=['Name', 'Age'])
from texttable import Texttable
t = Texttable()
t.add_rows([['Fruit', 'Price/Kg'], ['Apple', 25], ['Banana', 20]])
u=t
with open('me.txt','+w') as a:
    a.write(str(u))
