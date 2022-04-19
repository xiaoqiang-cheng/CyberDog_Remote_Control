import pyttsx3
engine = pyttsx3.init()

engine.setProperty('voice', 'zh')
engine.say("我叫小黑")
engine.runAndWait()