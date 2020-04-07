#!/usr/bin/env python
# coding: utf-8

# # NLTK Tokenizer

# In[2]:


# nltk postag list - https://medium.com/@gianpaul.r/tokenization-and-parts-of-speech-pos-tagging-in-pythons-nltk-library-2d30f70af13b
# CC coordinating conjunction
# CD cardinal digit
# DT determiner
# EX existential there (like: “there is” … think of it like “there exists”)
# FW foreign word
# IN preposition/subordinating conjunction
# JJ adjective ‘big’
# JJR adjective, comparative ‘bigger’
# JJS adjective, superlative ‘biggest’
# LS list marker 1)
# MD modal could, will
# NN noun, singular ‘desk’
# NNS noun plural ‘desks’
# NNP proper noun, singular ‘Harrison’
# NNPS proper noun, plural ‘Americans’
# PDT predeterminer ‘all the kids’
# POS possessive ending parent’s
# PRP personal pronoun I, he, she
# PRP$ possessive pronoun my, his, hers
# RB adverb very, silently,
# RBR adverb, comparative better
# RBS adverb, superlative best
# RP particle give up
# TO, to go ‘to’ the store.
# UH interjection, errrrrrrrm
# VB verb, base form take
# VBD verb, past tense took
# VBG verb, gerund/present participle taking
# VBN verb, past participle taken
# VBP verb, sing. present, non-3d take
# VBZ verb, 3rd person sing. present takes
# WDT wh-determiner which
# WP wh-pronoun who, what
# WP$ possessive wh-pronoun whose
# WRB wh-abverb where, when


# In[3]:


# https://www.nltk.org/book/ch05.html
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
import numpy as np
import cv2
# https://www.nltk.org/book/ch05.html
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
import nltk
from nltk import word_tokenize
import requests
import cv2
import os.path
from googletrans import Translator
from pytesseract import Output

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract



sanity_checkmark = ['CD', 'EX', 'JJ', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$', 'RB', 'VB', 'WDT', 'WP', 'WP$', 'WRB' ]

# punctuation, plural, adjective checking 

def pos_tag_sanity(text):
    text = word_tokenize(text)
    text = nltk.pos_tag(text)
    asl_text = []
    
    for i in range(len(text)):
        if text[i][1] in sanity_checkmark:
            asl_text.append(text[i][0])
            
    return asl_text

# print(pos_tag_sanity("And now is for something completely different. Eat were they"))    


# In[4]:


def listToStr(s):
    return ' '.join([str(elem) for elem in s]) 

def lettersToStr(s):
    return ''.join([str(elem) for elem in s]) 


# # Translate

# In[5]:


def gettranslation(text):
    translator = Translator()
    translated = translator.translate(text) 
    return translated.text

def detectlang(text):
    translator = Translator()
    detector = translator.detect(text)
    return detector.lang


# # Testing

# In[6]:


# text = word_tokenize("man men")
# print(nltk.pos_tag(text))

# pos_tag_sanity('dog dogs')

text = (pytesseract.image_to_string(Image.open('test_6.jpg'))).lower()
language = detectlang(text)
if language != "en":
    print('text',gettranslation(text))
    print('lang',language)
else:    
    print('here',text)
# print('text',text)

# print('pos_tag_sanity',pos_tag_sanity(text))
# text = word_tokenize(text)
# print(nltk.pos_tag(text))


# # AR Portion

# In[7]:


# https://www.learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/
#show-webcam-and-video-simultaneously
def showvideo2(c,caption):
    
    cv2.destroyAllWindows()
    
    global dim, font
    cap_video = cv2.VideoCapture(c)    

    # Check if camera opened successfully
    if (cap_video.isOpened()== False):
        print("Error opening video stream or file")
        
    while(cap_video.isOpened()):
        ret, frame = cap_video.read()
        ret_cam, frame_cam = cap.read()
        if ret == True and ret_cam== True :
            frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            frame_cam = cv2.resize(frame_cam, dim, interpolation = cv2.INTER_AREA)
            
            # Using cv2.putText() method 
            #https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/
            frame = cv2.putText(frame, caption, (50, 450), font,  
                               0.5, (255, 255, 255), 2, cv2.LINE_AA) 
        
            img3 = cv2.hconcat([frame,frame_cam])   
            cv2.imshow(WindowName,img3)
            cv2.moveWindow(WindowName, 0, 0)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
#         else:
        if ret != True:
            frame = None
            break

            
    cap_video.release()    
    cv2.destroyAllWindows()


# In[13]:


WindowName="Main View"
dim = (500, 500)
loading_img = cv2.imread('loading.jpg', cv2.IMREAD_COLOR )  
loading_img = cv2.resize(loading_img, dim, interpolation = cv2.INTER_AREA) 

# https://stackoverflow.com/a/54059166
def boundary_mark(frame):
    global dim
    d = pytesseract.image_to_data(frame, output_type=Output.DICT)
    n_boxes = len(d['level'])
    for i in range(1,n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA) 
    
    return frame
   
# https://www.learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/
def showvideo(c,frame_cam,caption):
    
    cv2.destroyAllWindows()
    
    cap_video = cv2.VideoCapture(c)    

    # Check if camera opened successfully
    if (cap_video.isOpened()== False):
        print("Error opening video stream or file")
        
    while(cap_video.isOpened()):
        ret, frame = cap_video.read()
        if ret == True:
            frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            
            # Using cv2.putText() method 
            #https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/
            frame = cv2.putText(frame, caption, (50, 450), cv2.FONT_HERSHEY_SIMPLEX , 0.5, (255, 255, 255), 2, cv2.LINE_AA) 
        
            img3 = cv2.hconcat([frame,frame_cam])   
            cv2.imshow(WindowName,img3)
            cv2.moveWindow(WindowName, 0, 0)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
#         else:
        if ret != True:
            frame = None
            break

            
    cap_video.release()    
    cv2.destroyAllWindows()    


def find_words(frame,loading_img=loading_img):
    
    f = open('non_ASL_word_list.txt', 'r')
    nonASLwords = f.readlines()
    f.close()   
       
    text = (pytesseract.image_to_string(frame)).lower()
        
    language = detectlang(text)
    if language != "en":
        text = gettranslation(text)
        
    frame_1 = boundary_mark(frame)
#     frame_1 = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    img3 = cv2.hconcat([loading_img,frame_1])
    
    modified_list_words = pos_tag_sanity(text)

    modified_urls = [ i + "/" + i + "-abc.mp4" if len(i) == 1 else i[0] + "/" + i + ".mp4" if i != "bye" else "bye-wave.mp4" for i in modified_list_words]
        
    print(modified_list_words,modified_urls)
    # Read URLs from handspeak.com
    # https://github.com/esqu1/ASLetter    
    for i, url in enumerate(modified_urls):
        
        cv2.imshow(WindowName,img3)
        cv2.moveWindow(WindowName, 0, 0)
        cv2.waitKey(delay = 1)
                
        if url in nonASLwords:
            print('trying_dict')
            letters = list(modified_list_words[i])
            for j, l in enumerate(letters):
                if l.isalpha():
                    showvideo("letters/%s-abc.mp4" % l,frame_1, listToStr(modified_list_words[:i])+" "+ lettersToStr(letters[:j]) + "*"+ l + "*"+
                                                     lettersToStr(letters[(j+1):]) +" "+ listToStr(modified_list_words[(i+1):])) 
                    
        elif os.path.isfile("data/" + url):
            print("playing existing video")
            showvideo("data/" + url, frame_1,listToStr(modified_list_words[:i])+" *"+ modified_list_words[i] + "* "+ listToStr(modified_list_words[(i+1):])) 
        else:    
            r = requests.get("https://handspeak.com/word/" + url)
            if r.text[:15] == "<!DOCTYPE html>":
                nonASLwords.append(url)
                letters = list(modified_list_words[i])
                
                for j, l in enumerate(letters):
                    if l.isalpha():
                        showvideo("letters/%s-abc.mp4" % l, frame_1,listToStr(modified_list_words[:i])+" "+ lettersToStr(letters[:j]) + "*"+ l + "*"+
                                                     lettersToStr(letters[(j+1):]) +" "+ listToStr(modified_list_words[(i+1):])) 
                        
            else: 

                f = open("data/" + url, 'wb')
                for chunk in r.iter_content(chunk_size=255):
                    if chunk:
                        f.write(chunk)
                f.close()
                showvideo("data/" + url, frame_1,listToStr(modified_list_words[:i])+" *"+ modified_list_words[i] + "* "+ listToStr(modified_list_words[(i+1):])) 


def main():
    cap = cv2.VideoCapture(0)

    count = 0
    while True:
        ret, frame = cap.read()
        count += 1
        if count%200 == 0:
            count = count%200
#             find_words(cv2.imread('test_7.jpg'))
            find_words(frame)
        if not ret:
            print("Unable to capture video")
            break 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break            

        frame_1 = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)   

        # Horizontally concatenate the 2 images
        img3 = cv2.hconcat([loading_img,frame_1])

        # Display the concatenated image
        cv2.imshow(WindowName,img3)
        cv2.moveWindow(WindowName, 0, 0)
    cap.release()
    cv2.destroyAllWindows()


# # Gui

# In[14]:


# https://www.geeksforgeeks.org/python-face-recognition-using-gui/
import tkinter as tk 
from tkinter import Message, Text 
from PIL import ImageTk 
import tkinter.ttk as ttk 
import tkinter.font as font


window = tk.Tk() 
# https://yagisanatode.com/2018/02/23/how-do-i-change-the-size-and-position-of-the-main-window-in-tkinter-and-python-3/
window.geometry("750x400") #Width x Height
window.title("AR_ASL") 
window.configure(background ='white') 
window.grid_rowconfigure(0, weight = 1) 
window.grid_columnconfigure(0, weight = 1) 
message = tk.Label( 
    window, text ="Language should not be a barrier.", 
    bg ="green", fg = "white", width = 32, 
    height = 3, font = ('times', 30, 'italic')) 

message.place(x = 20, y = 20) 

message_1 = tk.Label( 
    window, text ="Click Start to begin the journey", 
    bg ="white", fg = "black", width = 30, 
    height = 3, font = ('times', 30, 'bold')) 

message_1.place(x = 20, y = 150) 

takeImg = tk.Button(window, text ="Start", 
command = main, fg ="white", bg ="green", 
width = 20, height = 3, activebackground = "Red", 
font =('times', 15, ' bold ')) 
takeImg.place(x = 20, y = 300) 

quitWindow = tk.Button(window, text ="Quit", 
command = window.destroy, fg ="white", bg ="green", 
width = 20, height = 3, activebackground = "Red", 
font =('times', 15, ' bold ')) 
quitWindow.place(x = 480, y = 300) 

window.mainloop()


# In[ ]:




