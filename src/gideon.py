# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 21:16:30 2021

@author: Greekshith
"""

import pyttsx3

from VAapp import VAapp

# main
if __name__ == "__main__":
    # initializing an engine to set the voice type
    # can be changed to either a male or a female voice
    # voices[1] is for female voice
    # voices[0] is for male voice
    # no other indexes work for voices
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    app = VAapp()
    app.build()
    app.run()
