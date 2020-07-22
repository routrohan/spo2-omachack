import warnings
import pyrebase
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from utils import base64_to_pil_image, pil_image_to_base64
import re
import cv2
import numpy as np
from flask import Flask, request
from flask_restful import Resource, Api



app = Flask(__name__)
api = Api(app)
 
class testabusive(Resource):
	def get(self, user_index):
		
		
		config = {
								"apiKey": "AIzaSyBE8GNzn3pGAGo4yi0ElbF3pWohqDY3pWA",
  								"authDomain": "project-televital-3ac48.firebaseapp.com",
								"databaseURL": "https://project-televital-3ac48.firebaseio.com",
								"projectId": "project-televital-3ac48",
								"storageBucket": "project-televital-3ac48.appspot.com",
								"messagingSenderId": "706087011192",
								"appId": "1:706087011192:web:05d50bcb47b13eff0b3e8d"


		}

		firebase = pyrebase.initialize_app(config)
		db = firebase.database()
		#print(db)
		
		
		
		#print(res['spbase64'])
		#print(res['rr'])
		count = 0
		i=0
		A=100
		B=5
		bo = 0.0
		nm = db.child("Appointments").child(user_index).get()
		res= nm.val()
		video_frames = res['spbase64']
		video_strings = video_frames.split(';')
		video_strings = video_strings[1:]
		#print(video_strings[0]==video_strings[4])
		#video_strings = video_strings*2
		spresult = 0
		# convert it to a pil image
		spcount=0
		result= 0
		length = len(video_strings)
		print("The no of video_strings: "+str(length))
		for w in range(len(video_strings)):

					input_img = base64_to_pil_image(video_strings[w])


					input_img = input_img.resize((640,480))

					img  = cv2.cvtColor(np.array(input_img), cv2.COLOR_BGR2RGB)

					gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
					avg = 0
					count =0
					sumres = 0
					c1 = 0
					res=0
					rows,cols = gray.shape
					for i in range(rows):
						for j in range(cols):
							l = gray[i,j]
							avg = avg+l
							c1+=1
					for i in range(285,386):
					    for j in range(177,351):
					        k = gray[i,j]
					        # if i >= 285 and j >= 180 and i<=385 and j<=350:	
					        count +=1
					        sumres = sumres+k


					avg = avg/c1
					sumres = sumres/count
					avg = round(avg,0)
					sumres = round(sumres,0)
					print("photo avg: "+str(avg))
					print("Fin avg:" +str(sumres))
					diff = avg-sumres
					diff = abs(diff)
					#print(diff)

					# if diff >= 5:
					if avg >= 140:
						if sumres >=140 and sumres <=200:
							#print("Hand detected")
							res=1

						
					elif avg>=120 and avg<=139:
						if sumres >=130 and sumres <=200:

							#print("Hand detected")
							res=1
						else:

							#print("no hand")
							res=0

					elif avg>=90 and avg<=119:
						if sumres>=90 and sumres<=180:
							#print("hand detected")
							res=1

						else:
							#print("no hand")
							res=0

					else:
							#print("no hand")
							res=0
						
					# else:
					# 	print("No hand")
					# 	res=0

					print("res", str(res))	
					#res = 1
					if res == 1:

							#Red channel operations
							red_channel = img[:,:,2]
							mean_red = np.mean(red_channel)
							#print("RED MEAN", mean_red)
							std_red = np.std(red_channel)
							#print("RED STD", std_red)
							red_final = std_red/mean_red
							#print("RED FINAL",red_final)


							#Blue channel operations
							blue_channel = img[:,:,0]
							mean_blue = np.mean(blue_channel)
							#print("BLUE MEAN", mean_blue)
							std_blue = np.std(red_channel)
							#print("BLUE STD", std_blue)
							blue_final = std_blue/mean_blue
							#print("BLUE FINAL",blue_final)


							sp = A-(B*(red_final/blue_final))
							sp = round(sp,2)
							spresult = spresult+sp
							spcount +=1

					else:
							sp= "Finger not found"



					result = result+res

		
			
		result = result/length
		#result = 1
		print("final res value: "+ str(result))
		print("positive hand counts: "+ str(spcount))

		if result > 0.25:
			spresult = spresult/spcount
			spresult = round(spresult,2)
		else:
			spresult = "Finger not recognised"
		
		db.child("Appointments").child(user_index).update({"spo2":spresult})
		db.child("Consultation").child(user_index).update({"fspo2":spresult})
		return (1)

		# return (sp)	 
		# yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

		
		

api.add_resource(testabusive, '/spo/<user_index>')

if __name__ == '__main__':
   app.run()
