# AR-ASL

Language should not be a barrier to communication or education. People with difficulties in talking and listening face a lot of problem to communicate with others. They might have a hard time in reading textbooks or understanding foreign language. AR-ASL is a realtime application designed for these people to make their lives easier, with AR-ASL they can read books in realtime. AR-ASL also allows them understand foreign books and booklets without the intervention of others.  

![](/examples/3.PNG)

## Functionalities
1. Extract text from images in realtime
2. Translate to English automatically if the language is different
3. Tokenize and discard invalid words in Sign Language
4. Fetch the corresponding Sign Language video from [HandSpeak](https://www.handspeak.com/) Online dictionary
5. Play the video in realtime with marked up subtitle

## Requirements
1. Pytesseract
2. OpenCV
3. NLTK
4. GoogleTrans
5. tkinter

## How to Run
Run the following command after installing the requirements and follow the instruction in the menupage.

`python text_to_asl.py`

## Example of Working Demo
1. ASL from textbook, the word being animated is quoted in the subtitle:
![ASL from textbook, the word being animated is quoted in the subtitle](/examples/2.PNG)

2. ASL from Spanish Quote after translation
![ASL from Spanish Quote after translation](/examples/5.PNG)


## Future Work
1. Incorporating a 3D avatar instead of Human avatar
