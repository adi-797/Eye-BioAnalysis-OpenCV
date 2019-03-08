from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render
import numpy as np, cv2, os, imutils, datetime, time, csv
from statistics import mode
from tkinter import *
from pyzbar import pyzbar
from imutils.video import VideoStream
import argparse
import datetime
from pandas import DataFrame
from twilio.rest import Client 
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def direct_test(request):
    return render(request, 'direct_text.html')

def whatsapppost(a,b):
    account_sid = 'ACcd5aa4fc4ca8886844db39d149363f36' 
    auth_token = '602f6db1dd1bd228c84dcbe15f929df1' 
    client = Client(account_sid, auth_token) 
     
    message = client.messages.create( 
                                  from_='whatsapp:+14155238886',  
                                  body='Please have your ' + str(a) + ' medicine ' + str(b) + ' times today.',      
                                  to='whatsapp:+918375059963' 
                              )

def login(request):
    if 'Username' and 'Password' in request.GET:
        username_log = request.GET['Username']
        password_log = request.GET['Password']

        user_auth = 0

        with open('auth.csv', 'r') as f:
            read = csv.reader(f)
            for row in read:
                if row != []:
                    if (str(password_log) + '+' + str(username_log)) in str(row[0]):
                        f.close()
                        user_auth = 1
                        break

        if user_auth == 1:
            f = open('session.csv', "w+")
            f.close()
            with open('session.csv', 'a') as f:
            	f.write(str(password_log) + '+' + str(username_log))
            pass
        else:
            return HttpResponse("Incorrect credentials.")

        passvar = { 'user': username_log, 'pass' : password_log
        }



    else:
        return HttpResponse("Incorrect credentials.")
    return render(request, 'dashboard.html', passvar )

def login_only_redirect(request):
    if 'Username' and 'Password' in request.GET:
        username_log = request.GET['Username']
        password_log = request.GET['Password']

        user_auth = 0

        with open('auth.csv', 'r') as f:
            read = csv.reader(f)
            for row in read:
                if row != []:
                    if (str(password_log) + '+' +str(username_log)) in str(row[0]):
                        f.close()
                        user_auth = 1
                        break

        if user_auth == 1:
            f = open('session.csv', "w+")
            f.close()
            with open('session.csv', 'a') as f:
            	f.write(str(password_log) + '+' + str(username_log))
            f.close()
            pass
        else:
            return HttpResponse("Incorrect credentials.")
        
        passvar = { 'user': username_log, 'pass' : password_log
        }

    else:
        return HttpResponse("Incorrect credentials.")
    return render(request, 'dashboard.html', passvar )

def genform(request):
    return render(request, 'genform.html')

def notifyform(request):
    return render(request, 'notifyform.html')

def notifyformexec(request):
    if 'medi' and 'times' in request.GET:
        a = request.GET['medi']
        b = request.GET['times']
        whatsapppost(a,b)
        
        return render(request, 'dashboard.html')
    else:
        return HttpResponse("failed.")

def diagnosis_registered(request):
    return render(request, 'diagnosis_registered.html')

def signup(request):
    if 'emailid' and 'username' and 'date' and 'phone' and 'password' and 'confirmpass' in request.GET:
	    emailid = request.GET['emailid']
	    username = request.GET['username']
	    date = request.GET['date']
	    phone = request.GET['phone']
	    password = request.GET['password']
	    confirmpass = request.GET['confirmpass']

	    if password != confirmpass:
	        return HttpResponse('Password do not match! Retry.')

	    else:
	        with open('auth.csv', 'a') as f:
		        f.write(str(password) + '+' + str(username) + ': bil*\n')
		        f.write(str(password) + '+' + str(username) + ': cat*\n')
		        f.write(str(password) + '+' + str(username) + ': chol*\n')

		        f.close()

	        return render(request, 'login_only.html')
    else:
        return HttpResponse('Incorrect password! Retry.')

def decode(im):
    #Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    uid = ""
    name = ""

    #Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data, '\n')
        details = str(obj.data)
        for i in range(len(str(obj.data))):
            # print(str(obj.data[i:i+4]))
            if(details[i:i+3]=="uid"):
                j = i + 5
                temp = ""
                while(True):
                    temp = str(temp) + str(details[j])
                    j = j + 1
                    if details[j] == '"':
                        uid = str(temp)
                        break
            if(details[i:i+4])=="name":
                j = i + 6
                temp = ""
                while(True):
                    temp = str(temp) + str(details[j])
                    j=j+1
                    if details[j] == '"':
                        name = str(temp)
                        break

    return uid, name


def aadhar(request):   

    from tkinter import filedialog

    uid = ""
    name = ""

    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()

    if file_path is not "" and (".png" in file_path or ".jpeg" in file_path or ".jpg" in file_path or ".JPG" in file_path or ".PNG" in file_path):
        im = cv2.imread(file_path)
        uid, name = decode(im)
        passvar = {'pass': uid, 'user': name}
        
        with open('auth.csv', 'a') as f:
        	f.write(str(uid) + '+' + str(name) + ': bil:*\n')
        	f.write(str(uid) + '+' + str(name) + ': cat:*\n')
        	f.write(str(uid) + '+' + str(name) + ': chol:*\n')

        f.close()
        return render(request, 'dashboard.html', passvar)

    else:
        return HttpResponse('Failed. Please upload the right file.')

def aadhar2(request):
    try:
        vs = VideoStream(src=1).start()
    except:
        vs = VideoStream(src=0).start()

    time.sleep(2.0)
    found = set()
    text = 'q'
    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)
        # loop over the detected barcodes
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # if the barcode text is currently not in our CSV file, write
            # the timestamp + barcode to disk and update the set
            if barcodeData not in found:
                found.add(barcodeData)
                # show the output frame

        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF

                # if the `q` key was pressed, break from the loop
        if text is not "q":
            break

    cv2.destroyAllWindows()
    vs.stop()

    details = text
    print (text)
    for i in range(len(str(text))):
        # print(str(obj.data[i:i+4]))
        if(details[i:i+3]=="uid"):
            j = i + 5
            temp = ""
            while(True):
                temp = str(temp) + str(details[j])
                j = j + 1
                if details[j] == '"':
                    uid = str(temp)
                    break
        if(details[i:i+4])=="name":
            j = i + 6
            temp = ""
            while(True):
                temp = str(temp) + str(details[j])
                j=j+1
                if details[j] == '"':
                    name = str(temp)
                    break

    try:
    	passvar = {'pass': uid, 'user': name}
    except:
    	return HttpResponse('Aadhar barcode uid invalid. Please show an alternate copy.')

    with open('auth.csv', 'a') as f:
    	f.write(str(uid) + '+' + str(name) + ': bil:*\n')
    	f.write(str(uid) + '+' + str(name) + ': cat:*\n')
    	f.write(str(uid) + '+' + str(name) + ': chol:*\n')

    f.close()
    return render(request, 'dashboard.html', passvar)
    

def search_form(request):
    return render(request, 'search-form.html')

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm.NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm.NameForm()

    return render(request, 'name.html', {'form': form})

def nothing(temp):
    pass

def camera():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    face_cascade = cv2.CascadeClassifier(os.path.join(BASE_DIR, 'haarcascade_frontalface_alt.xml'))

    try:
        camera=cv2.VideoCapture(0)
    except:
        camera = cv2.VideoCapture(1)

    numerator=0
    denominator=0

    pupil = []

    while True:

        ret, frame = camera.read()
        frame_copy = frame
        roi=frame
        frame=cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        coordinates_eye = []

        for (x,y,w,h) in faces:
            coordinates_eye.append((x,y,w,h))
    ##        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
            #cv2.line(frame,(int(x+w/2),int(y)),(int(x+w/2),int(y+h/2)),(255,0,0),1)
            #cv2.line(frame,(int(x+w/4.2),int(y+h/2.2)),(int(x+w/2.5),int(y+h/2.2)),(0,255,0),1)
            #cv2.line(frame,(int(x+w/4.2),int(y+h/3)),(int(x+w/2.5),int(y+h/3)),(0,255,0),1)
            cv2.line(frame,(int(x+w/4.2),int(y+h/3)),(int(x+w/4.2),int(y+h/2.2)),(0,255,0),1) #left
            cv2.line(frame,(int(x+w/2.5),int(y+h/3)),(int(x+w/2.5),int(y+h/2.2)),(0,255,0),1) #right
            
            #------------ estimation of distance of the human from camera--------------#
            d=10920.0/float(w)

            #-------- coordinates of interest --------------# 
            x1=int(x+w/4.2)+1       #-- +1 is done to hide the green color
            x2=int(x+w/2.5)
            y1=int(y+h/3)+1
            y2=int(y+h/2.2)
            roi=frame[y1:y2,x1:x2]
            gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
            equ = cv2.equalizeHist(gray)
            thres=cv2.inRange(equ,0,20)
            kernel = np.ones((3,3),np.uint8)
            #/------- removing small noise inside the white image ---------/#
            dilation = cv2.dilate(thres,kernel,iterations = 2)
            #/------- decreasing the size of the white region -------------/#
            erosion = cv2.erode(dilation,kernel,iterations = 3)
            #/-------- finding the contours -------------------------------/#
            contours, hierarchy = cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            #--------- checking for 2 contours found or not ----------------#
            if len(contours)==2 :
                numerator+=1
                #img = cv2.drawContours(roi, contours, 1, (0,255,0), 3)
                #------ finding the centroid of the contour ----------------#
                M = cv2.moments(contours[1])
                #print M['m00']
                #print M['m10']
                #print M['m01']
                if M['m00']!=0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    pupil.append((cx,cy))
                    cv2.line(roi,(cx,cy),(cx,cy),(255,0,255),10)
                    
                #print cx,cy
            #-------- checking for one countor presence --------------------#
            elif len(contours)==1:
                numerator+=1
                #img = cv2.drawContours(roi, contours, 0, (0,255,0), 3)

                #------- finding centroid of the countor ----#
                M = cv2.moments(contours[0])
                if M['m00']!=0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    pupil.append((cx,cy))
                    #print cx,cy
                    cv2.line(roi,(cx,cy),(cx,cy),(0,0,255),20)
        
            else:
                denominator+=1
                #print "iris not detected"            
    
        cv2.putText(frame,'Press "ESC" to capture.',(20,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2,cv2.LINE_AA)
        cv2.imshow("frame",frame)
        
        #cv2.imshow("eye",image)
        if cv2.waitKey(30)==27 & 0xff:
            ret1 = cx
            ret2 = cy
            ret, sample = camera.read()
            break
    camera.release()
    #print ("accurracy=",(float(numerator)/float(numerator+denominator))*100)
    cv2.destroyAllWindows()

    x2 = 0
    y2 = 0

    try:
        a = mode([x for x in range(len(pupil))])

        for i in range(len(pupil)):
            if pupil[i][0] - a[0] > 20 or pupil[i][1] - a[1]>20:
                 pupil.remove(i+1)

    except:
        pass

    for index in range(len(pupil)):

            x2+= pupil[index][0]
            y2+= pupil[index][1]


    cx, cy = 0,0
    cx = x2/len(pupil)
    cy = y2/len(pupil)

    return sample,ret1,ret2

def cholesterol(sample, cx,cy):
    sample = imutils.resize(sample, width=640)
    blur = cv2.medianBlur(sample,5)
    bil = cv2.bilateralFilter(blur,5,1000,1000)

    y = cy-23
    h = 50
    x = cx - 60
    w = 90

    try:

        gray = cv2.cvtColor(bil,cv2.COLOR_BGR2GRAY)

        # Center and radius detection of pupil.
        pupil_center = (cx, cy)
        pupil_radius = 5
        cv2.circle(sample, pupil_center, pupil_radius, (0,0,255), 2)

        # Multiplier based on general ratio of radius of iris to pupil.
        iris_radius = pupil_radius*4
        
        cv2.circle(sample,pupil_center,iris_radius , (0,0,255), 2)

        # Finding the minimum bounded rectangle.
        cv2.circle(sample,pupil_center,iris_radius , (255,255,255), -1)

        # Cropping to a standard size.

        mask = np.zeros(sample.shape, dtype = "uint8")
        cv2.circle(mask,pupil_center,iris_radius , (255,255,255), -1)
        mask = mask[y:y+h, x:x+w]
        mask = cv2.resize(mask, (240,240))
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        copy_orig = copy_orig[y:y+h, x:x+w]
        copy_orig = cv2.resize(copy_orig, (240,240))
        res = cv2.bitwise_and(copy_orig,copy_orig, mask = mask)

        cv2.imshow("a", res)
        cv2.imshow("abb", sample)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        ##res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        ##imga = np.asarray(res,dtype=np.float64)
        ##pol = topolar(imga)
        # Output Image for nomarlized iris.
        ##cv2.imshow('Normalize', pol)

        y, x = res.shape[:2]
        total = 0
        mat = 0
        for i in range(x):
            for j in range(y):
                arr = res[j, i]
                if (abs(arr[0]-arr[1])<=10) and (abs(arr[1]-arr[2])<=10) and (abs(arr[2]-arr[1]) <= 10):
                    mat+=1
                total+=1

        ratio_of_grey = mat/total

    except:
        ratio_of_grey = 0.1

    #return ratio_of_grey
    if ratio_of_grey>= 0.2 and ratio_of_grey<= 0.35:
        pr = "MILD"
    elif ratio_of_grey> 0.35:
        pr = "HIGH"
    else:
        pr = "NORMAL"

    return pr

def bilirubin(sample, cx,cy):
    image = imutils.resize(sample, width=640, height=480)
    image = cv2.medianBlur(image,5)
    image = cv2.bilateralFilter(image,5,1000,1000)
   # image = image[c] TODO
    frame = image.copy()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_yel = np.array([20,50,120]) #all shades of yellow
    upper_yel = np.array([60,255,255])
    mask = cv2.inRange(hsv, lower_yel, upper_yel)
    res = cv2.bitwise_and(frame,frame, mask = mask)
    image = res.copy()
    res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    y, x = res.shape[:2]
    total = 0
    mat = 0
    for i in range(x):
        for j in range(y):
            arr = res[j, i]
            if arr == 0:
                continue
            mat+=1
            total+=arr

    average = float(total)/float(mat)
    average = 1- np.interp(average, [0,255], [0,1])

    return average


def cataract(sample, cx,cy):
    image = imutils.resize(sample, width=640, height=480)
    image = cv2.medianBlur(image,5)
    #image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image = cv2.bilateralFilter(image,5,1000,1000)
    # image2 = [cx-80: cx+80, cy-20:cy+40]
    arr = []
    mat = 0
    try:
        for i in range(cx - 5,cx + 5):
            for j in range(cy - 5,cy + 5):
                #color.append(image[j,i])
                arr = image[j,i]
                if (abs(arr[0]-arr[1])<=10) and (abs(arr[1]-arr[2])<=10) and (abs(arr[2]-arr[1]) <= 10):# and arr[0] < 220 and arr[1] < 220 and arr[2] < 220:
                   mat+=1
        mat = mat + 3
    except:
        mat = 10

    return mat

def log_med_data(tag, data):
	with open('session.csv', 'r') as f:
            read = csv.reader(f)
            for row in read:
                if row != []:
                	ptr = str(row[0])

	f.close()

	with open('auth.csv', 'r') as f:
		read = csv.reader(f)
		i = 0
		for row in read:
			if row != []:
				if (ptr) in row[0] and str(tag) in row[0]:
					index = i
					f.close()
					bottle_list = []

					with open('auth.csv', 'r') as b:
						bottles = csv.reader(b)
						bottle_list.extend(bottles)
					line_to_override = {index:[row[0]+str(data)+'*'] }
					f = open('auth.csv', "w+")
					f.close()

					with open('auth.csv','a') as f:
						for line, row in enumerate(bottle_list):
							data = line_to_override.get(line, row)
							if data != []:
								f.write(str(data[0])+'\n')

					b.close()
					break
			i+=1



def bilirubin_login(request):
    sample_frame, cx, cy = camera()

    bilirubin_level = bilirubin(sample_frame, cx, cy)

    log_med_data('bil', (bilirubin_level*3 + bilirubin_level*9) / 2)

    rang = str(bilirubin_level*3) + ' to ' + str(bilirubin_level*9) + ' mg/dl'
    rang = str(rang)

    return render(request, 'result.html', {'value' : rang })


def cataract_login(request):
    sample_frame, cx, cy = camera()

    cataract_level = cataract(sample_frame, cx, cy)

    log_med_data('cat', cataract_level)

    cataract_level = "Percentage = " + str(cataract_level) + " %"
    cataract_level = str(cataract_level)

    return render(request, 'result.html', {'value' : cataract_level })


def cholesterol_login(request):
    sample_frame, cx, cy = camera()

    cholesterol_level = cholesterol(sample_frame, cx, cy)

    log_med_data('chol', cholesterol_level)

    return render(request, 'result.html', {'value' : cholesterol_level })

def bilirubin_(request):
    sample_frame,cx,cy = camera()

    bilirubin_level = bilirubin(sample_frame,cx,cy)

    rang = str(bilirubin_level*3) + ' to ' + str(bilirubin_level*9) + ' mg/dl'
    rang = str(rang)

    return render(request, 'result.html', {'value' : rang })

def cataract_(request):
    sample_frame,cx,cy = camera()

    cataract_level = cataract(sample_frame,cx,cy)

    cataract_level = "Percentage = " + str(cataract_level) + " %"
    cataract_level = str(cataract_level)

    return render(request, 'result.html', {'value' : cataract_level })

def cholesterol_(request):
    sample_frame,cx,cy = camera()

    cholesterol_level = cholesterol(sample_frame,cx,cy)

    return render(request, 'result.html', {'value' : cholesterol_level })

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def logout(request):
	f = open('session.csv', "w+")
	f.close()
	return render(request, 'search-form.html')

def history(request):
	with open('session.csv', 'r') as f:
            read = csv.reader(f)
            for row in read:
                if row != []:
                	ptr = str(row[0])

	f.close()

	with open('auth.csv', 'r') as f:
		read = csv.reader(f)
		i = 0
		count  = 0
		for row in read:
			if row != []:
				if ptr in row[0]:
					if 'bil' in row[0]:
						bil_gr = str(row[0])
						start = bil_gr.index('*')
						num = ''
						num_list = []
						i = start+1
						while i < len(bil_gr):
							if bil_gr[i] == '*':
								num_list.append(float(num))
								num = ''
								i+=1

							if i < len(bil_gr):
								num+= bil_gr[i]
							i+=1
					if 'cat' in row[0]:
						bil_gr = str(row[0])
						start = bil_gr.index('*')
						num = ''
						num_list2 = []
						i = start+1
						while i < len(bil_gr):
							if bil_gr[i] == '*':
								num_list2.append(float(num))
								num = ''
								i+=1

							if i < len(bil_gr):
								num+= bil_gr[i]
							i+=1

					if 'chol' in row[0]:
						bil_gr = str(row[0])
						start = bil_gr.index('*')
						num = ''
						num_list3 = []
						i = start+1
						while i < len(bil_gr):
							if bil_gr[i] == '*':
								if num == 'NORMAL':
									temp_var = 1
								elif num == 'MILD':
									temp_var = 5
								else:
									temp_var = 10

								num_list3.append(temp_var)
								num = ''
								i+=1
							if i < len(bil_gr):
								num+= bil_gr[i]
							i+=1

	bil = mpatches.Patch(color='yellow', label='Bilirubin levels (mg/dl)')
	cat = mpatches.Patch(color='green', label='Cataract levels (%)')
	chol = mpatches.Patch(color='red', label='Cholesterol levels (NORMAL=1, MILD=5, HIGH=10')
	plt.legend(handles = [bil, cat, chol])
	plt.plot(num_list, 'y')
	plt.plot(num_list2, 'g')
	plt.plot(num_list3, 'r')
	plt.show()

	return HttpResponse('Done! Please click back button.')

def gen_diagnosis(request):

	try:
		element = request.GET['search']
		element = str(element).lower()

		if len(element) < 3 or element == 'and':
			return render(request, 'gen_diagnosis.html', {'flag2': 0, 'element': str(element)})

		with open('data.csv', 'r') as f:
			read = csv.reader(f)
			for row in read:
				if row != []:
					row_itr = str(row[0]).lower()
					if element in row_itr:
						ret = { 'flag': 1, 'deficiency':str(row[2]), 'food': str(row[1]), 'flag2':1 , 'element': str(row[0])}
						return render(request, 'gen_diagnosis.html', ret)
		return render(request, 'gen_diagnosis.html', {'flag2': 0, 'element': str(element)})

	except:
		try:
			helpp = request.GET['help']
			ret = []
			with open('data.csv', 'r') as f:
				read = csv.reader(f)
				for row in read:
					if row != []:
						ret.append(str(row[0]))
			return render(request, 'gen_diagnosis.html', { 'help': ret, 'flag3': 1})

		except:
			return render(request, 'gen_diagnosis.html', {'flag' : 0})

def finddoctors(request):
	try:
		city = request.GET['city']
		domain = request.GET['domain']
		city = str(city).lower()
		domain = str(domain).lower()

		doctors = []

		if city == 'none' or domain == 'none':
			return render(request, 'doctors.html', { 'flag': 0})

		with open('doctors.csv', 'r') as f:
				read = csv.reader(f)
				for row in read:
					if row[0] != []:
						if city in row[0] and domain in row[0]:
							for i in range(1, len(row)):
								doctors.append(str(row[i]))

		return render(request, 'doctors.html', {'flag': 1, 'doctors': doctors})

	except:
		return render(request, 'doctors.html', { 'flag': 0})


def diagnosis_option(request):
	try:
		option = request.GET['option']
		if option == 'YES':
			return render(request, 'diagnosis_module.html')
		else:
			return render(request, 'diagnosis_registered.html')
	except:
		return render(request, 'diagnosis_option.html')

def camera_module():
    try:
        camera=cv2.VideoCapture(1)
    except:
        camera = cv2.VideoCapture(0)

    while True:

        ret, frame = camera.read()
        frame_copy = frame
        roi=frame
        frame=cv2.flip(frame,1)        
    
        cv2.putText(frame,'Press "ESC" to capture.',(20,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2,cv2.LINE_AA)
        cv2.imshow("frame",frame)
        
        #cv2.imshow("eye",image)
        if cv2.waitKey(30)==27 & 0xff:
            ret, sample = camera.read()
            break
    camera.release()
    #print ("accurracy=",(float(numerator)/float(numerator+denominator))*100)
    cv2.destroyAllWindows()

    return sample

def cholesterol_login_module(request):
	sample = camera_module()

	return HttpResponse('ok')

def bilirubin_login_module(request):
	image = camera_module()
	image = imutils.resize(image, width=640, height=480)
	image = cv2.medianBlur(image,5)
	image = cv2.bilateralFilter(image,5,1000,1000)
	frame = image.copy()

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_yellow = np.array([18,40,120]) #all shades of yellow
	upper_yellow = np.array([60,255,255])
	mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
	res = cv2.bitwise_and(frame,frame, mask = mask)
	image = res.copy()
	res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
	y, x = res.shape[:2]
	total = 0
	mat = 0
	for i in range(x):
		for j in range(y):
			arr = res[j, i]
			if arr == 0:
				continue
			mat+=1
			total+=arr
	average = float(total)/float(mat) #per pixel intensity
	average = 1- np.interp(average, [0,255], [0,1])
	bil_val = ((((average*mat)/61440)/3.8)*100)

	return render(request, 'result.html', { 'value':  'Levels between ' + str(bil_val * 0.9) + ' and ' + str(bil_val * 1.1)})

def cataract_login_module(request):
	sample = camera_module()
	return HttpResponse('ok')
