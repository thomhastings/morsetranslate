#!/usr/bin/env python
#morsetranslate.py
#
#GUI app to translate between plain text and morse code notation 

from Tkinter import *
from morse import MorseTranslator

class MyApp(Frame):

    def __init__(self, master):

        self.translator = MorseTranslator() 
        
        #On Python 2.X Tkinter uses 'classic' classes
        #as a result base class cant be accessed with super()
        #but must be called with the base class name
        Frame.__init__(self, master)
        self.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        self._createWidgets()

    def _createWidgets(self):

        """Build the GUI widgets, pack the layout & bind event handlers"""

        
        defFont = ("Monospace", 12, "bold")

        #TOP FRAME--------------------------
        #Contains labels and IN_FRAME
        topFrame = Frame(self)
        topFrame.pack(fill=BOTH, side=TOP, expand=YES)

        inLabel = Label(topFrame,
                        text="Text",
                        relief=GROOVE,
                        width=6, 
                        anchor=CENTER,
                        font=defFont)

        inLabel.pack(side=TOP, anchor=NW)

        #IN FRAME
        #within TOP FRAME, contains upper Text widget & Scrollbar
        inFrame = Frame(topFrame)
        inFrame.pack(fill=BOTH, side=BOTTOM, expand=YES)

        plainTextScroll = Scrollbar(inFrame)
        plainTextScroll.pack(side=RIGHT, fill=Y)

        plainTextArea = Text(inFrame,
                            width=50,
                            height=5,
                            borderwidth=2, 
                            font=defFont,
                            yscrollcommand=plainTextScroll.set)
        
        plainTextArea.pack(side=RIGHT, fill=BOTH, expand=YES)
        plainTextScroll.config(command=plainTextArea.yview)

        #END TOP FRAME --------------------
        
        #Spacing frame between TOP FRAME and BOTTOM FRAME
        #contains RadioButtons to toggle text entry area
        seperator = Frame(self, bd=2, relief=GROOVE)
        seperator.pack(fill=NONE, padx=10, pady=10)
 
        button1 = Radiobutton(seperator,
                            text="Morse to Text",
                            value=1, 
                            indicatoron=0,
                            padx=5,
                            pady=5)
        
        button1.pack(side=BOTTOM, padx=3, pady=2)
        
        button2 = Radiobutton(seperator,
                            text="Text to Morse",
                            value=0,
                            indicatoron=0,
                            padx=5,
                            pady=5)

        button2.pack(side=BOTTOM, padx=3, pady=2)

        #BOTTOM FRAME----------------------
        #Contains label and OUT FRAME
        bottomFrame = Frame(self)
        bottomFrame.pack(fill=BOTH, side=TOP, expand=YES)
        
        outLabel = Label(bottomFrame,
                        text="Morse",
                        relief=GROOVE,
                        width=6,
                        anchor=CENTER,
                        font=defFont)

        outLabel.pack(side=TOP, anchor=NW)
        
        #OUT FRAME
        #Contains Text widget and it's associated scrollbar
        outFrame = Frame(bottomFrame)
        outFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)

        morseScroll = Scrollbar(outFrame)
        morseScroll.pack(side=RIGHT, fill=Y)

        morseTextArea = Text(outFrame,
                            width=50,
                            height=5,
                            borderwidth=2, 
                            font=defFont,
                            yscrollcommand=morseScroll.set)

        morseTextArea.pack(side=RIGHT, fill=BOTH, expand=YES)
        morseScroll.config(command=morseTextArea.yview)
        #END BOTTOM FRAME----------------------

        
        #Bind event handlers to Text and Radiobutton widgets
        #Lambda used to send different parameters to the
        #same event handlers
        #see self.UpdateText() & self._switchTextArea() below
        morseTextArea.bind("<KeyRelease>",
                            lambda event, 
                            arg1=plainTextArea,
                            arg2=self.translator.convertFromMorse:
                            self._updateText(event, arg1, arg2))

        plainTextArea.bind("<KeyRelease>",
                            lambda event,
                            arg1=morseTextArea,
                            arg2=self.translator.convertToMorse:
                            self._updateText(event, arg1, arg2))

        button1.config(command=lambda arg1=plainTextArea,
                                arg2=morseTextArea:
                                self._switchTextArea(arg1,arg2))
        
        button2.config(command=lambda arg1=morseTextArea,
                                arg2=plainTextArea:
                                self._switchTextArea(arg1,arg2))

        #set the Text to Morse mode at startup
        button2.invoke()

    def _updateText(self, event, out, func):

        """Refresh the contents of the output Text widget with the
        translation of the text from the input Text widget

        @event - Tk event object sent in by default when using event
        binding. Contains the identity of the widget that originated
        the event.  This is the input Text widget where a key was released

        @out - The widget on which to output the translation

        @func - The actual translations operation to perform. This
        is a function object.
        """
        
        #translate the text from event.widget, using the translation
        #operation func()
        outStr=func(event.widget.get(1.0, 'end'))

        #switch output widget from DISABLED to ENABLED to allow output
        #disable again after output to leave it in the same state it was
        #in before the update
        out.config(state=NORMAL)
        out.delete(1.0, 'end')
        out.insert(1.0, outStr)
        out.see('end')
        out.config(state=DISABLED)

    def _switchTextArea(self, toDisable, toActivate):
        
        """ Toggle which Text widget is active.  Active widget allows text
        entry, disabled one does not.

        @toDisable - reference to Text widget to be disabled

        @toActivate - reference to Text widget to make active
        """

        toDisable.delete(1.0, 'end')
        toDisable.config(state=DISABLED)
        toActivate.config(state=NORMAL)
        toActivate.delete(1.0, 'end')
        toActivate.focus_force()

root = Tk()
root.title("Morse Code Translator")

app = MyApp(root)
app.mainloop()

