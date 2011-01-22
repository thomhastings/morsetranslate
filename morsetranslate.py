#!/usr/bin/env python
#morsetranslate.py
#
#GUI app to translate between plain text and morse code notation 

from Tkinter import *
from morse import MorseTranslator
import platform

#Class combining a Label and Text Entry widget into Frame
#Abstracted away from the main app class createWidget function
#for the sake of simplicity and reducing code repetition when creating
#my Text and Label widgets
class TextEntryGroup(Frame):
    def __init__(self, master, name, font):
        Frame.__init__(self, master)

        self._name = name
        self._font = font
        #variable to hold the actual Text widget, instantiation in
        #createWidget
        self._textInputWidget = None
        self._createWidgets()

    def _createWidgets(self):

        """Create & pack the Text and Label widgets that make up this 
        TextEntryGroup."""

        nameLabel = Label(self,
                        text=self._name,
                        relief=GROOVE,
                        width=len(self._name), 
                        anchor=CENTER,
                        font=self._font
                        )

        nameLabel.pack(side=TOP, anchor=NW)

        inFrame = Frame(self)
        inFrame.pack(fill=BOTH, side=BOTTOM, expand=YES)

        textScroll = Scrollbar(inFrame)
        textScroll.pack(side=RIGHT, fill=Y)

        self._textInputWidget = Text(inFrame,
                            width=50,
                            height=5,
                            borderwidth=2, 
                            font=self._font,
                            yscrollcommand=textScroll.set)
        
        self._textInputWidget.pack(side=RIGHT, fill=BOTH, expand=YES)
        textScroll.config(command=self._textInputWidget.yview)


    def getTextWidget(self):

        """Return the Text widget instance of the TextEntryGroup"""
        
        return self._textInputWidget


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
        
        appFont = ("Monospace", 12, "bold")

        plainText = TextEntryGroup(self, "Text", appFont)
        plainText.pack(fill=BOTH, side=TOP, expand=YES)

        #Spacing frame between top TextEntryGroup and bottom TextEntryGroup 
        #contains RadioButtons to toggle text entry araea
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
        
        morseText = TextEntryGroup(self, "Morse", appFont)
        morseText.pack(fill=BOTH, side=TOP, expand=YES)

        #Bind event handlers to Text and Radiobutton widgets
        #Lambda used to send different parameters to the
        #same event handlers
        #see self.UpdateText() & self._switchTextArea() below
        morseText.getTextWidget().bind("<KeyRelease>",
                            lambda event, 
                            arg1=plainText.getTextWidget(),
                            arg2=self.translator.convertFromMorse:
                            self._updateText(event, arg1, arg2))

        plainText.getTextWidget().bind("<KeyRelease>",
                            lambda event,
                            arg1=morseText.getTextWidget(),
                            arg2=self.translator.convertToMorse:
                            self._updateText(event, arg1, arg2))

        button1.config(command=lambda arg1=plainText.getTextWidget(),
                                arg2=morseText.getTextWidget():
                                self._switchTextArea(arg1,arg2))
        
        button2.config(command=lambda arg1=morseText.getTextWidget(),
                                arg2=plainText.getTextWidget():
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

def setTitleIcon(tkinstance):
    """Detect the platform and set the appropriate title bar icon.  If
    OS can't be detected, or no appropriate icon file is present, no icon is
    set"""

    osStr = platform.system()

    if(osStr == "Windows"):
        tkinstance.iconbitmap('icon.ico')
        return True
    elif(osStr == "Linux"):
        tkinstance.iconbitmap('@icon.xbm')
        return True
    else:
        return False

root = Tk()

setTitleIcon(root)
root.title("Morse Code Translator")

app = MyApp(root)
app.mainloop()

