# python 3.6
import json
import os
import platform
import pydeepl as deepl  # https://github.com/EmilioK97/pydeepl/blob/master/pydeepl/pydeepl.py
import threading
import time

class Translator:



    def __isFile(self, object=None):
        if object == None:
            object = self.file
        try:
            os.listdir(object)
            return False
        except Exception:
            return True

    def autodir(self):
        try:
            directory = os.path.dirname(os.path.realpath(__file__))
            if platform.system() == 'Linux':
                slash = '/'
            elif platform.system() == 'Windows':
                slash = '\\'
            self.dir = directory + slash
            return True
        except Exception:
            self.dir = None
            return False

    def autofile(self):
        try:
            objects = os.listdir(self.dir)
            srtfiles = []
            try:
                for i in range(0, len(objects)):
                    try:
                        os.listdir(objects[i])
                    except Exception:
                        if objects[i].split(".")[-1] == "srt":
                            srtfiles.append(objects[i])
                try:
                    self.file = srtfiles[0]
                except Exception:  # no srt files found in the current directory
                    self.file = None
                    return False
            except Exception:  # no files found in the current directory (practical paradoxon)
                self.file = None
                return False
        except Exception:  # no directory selected
            self.file = None
            return False

    def __init__(self, dir=None, file=None):
        # define directory and automaticly fill if possible
        if dir == None: self.autodir()
        else: self.dir = str(dir)

        # define file and automaticly fill if possible
        if file == None:
            self.autofile()
        else:
            self.file = str(file)

        # define other
        self.filecontent = []
        self.interpreted = json.loads('{}')
        self.translated = json.loads('{}')
        self.fromlang = "auto"
        self.tolang = "DE" #['DE', 'EN', 'FR', 'ES', 'IT', 'NL', 'PL']
        self.threadtime = 0.3  # (in seconds)   change this to a higher value if you get a "TranslationError DeepL call resulted in a unknown result." and wait some time to retry.

    def __repr__(self):
        return str(self.dir + self.file)

    def setdir(self, dir):
        try:
            os.listdir(dir)
            self.dir = dir
            return dir
        except Exception:
            pass

    def setfile(self, file):
        try:
            open(self.dir+str(file))
            self.file = file
            return file
        except Exception:
            pass

    def _check(self):
        try:
            os.listdir(self.dir)
            try:
                open(self.dir + self.file, "r")
                return True, "Checked!"
            except Exception:
                return False, "Failed to read file!"
        except Exception:
            return False, "Failed to read directory!"

    def splithtml(self, string):
        string = str(string)
        splitten = [""]
        for i in range(0, len(string)):
            if string[i] == "<":
                splitten.append("<")
            elif string[i] == ">":
                splitten[-1] = splitten[-1] + ">"
                if i != len(string) - 1:
                    splitten.append("")
            else:
                splitten[-1] = splitten[-1] + string[i]
        return splitten

    def removehtml(self, content):
        if not content is list:
            content = self.splithtml(content)
        string = ""
        if len(content) != 0:
            for i in range(0, len(content)):
                try:
                    if not content[i][0] == "<":
                        string += content[i]
                except Exception:
                    pass
            return string
        else:
            return content

    def ishtml(self, string):
        if string[0] == "<":
            return True
        else:
            return False

    def readfile(self):
        filename = open(self.dir + self.file, "r", encoding='utf-8')
        content = filename.readlines()
        filename.close()
        content.insert(0, "\n")

        for i in range(0, len(content)):  # remove BOM
            content[i] = content[i].replace('\ufeff', "")
        for i in range(0, len(content)): # removing html
            content[i] = self.removehtml(content[i].rstrip())

        self.filecontent = content
        return content

    def buildstring(self, ls, spacer):
        string = ""
        for i in range(0, len(ls)):
            string = string + str(spacer) + str(ls[i])
        return string

    def interprete(self):
        frames = []
        for i in range(0, len(self.filecontent)):
            if self.filecontent[i].rstrip() == "":  # create a new sublist, when there is a free line (start of a new subtitle-frame)
                frames.append([])
            else:  # append content to the latest sublist
                frames[len(frames) - 1].append(self.filecontent[i].rstrip())

        for i in range(0, len(frames)): # create json data
            self.interpreted[frames[i][0]] = {}
            self.interpreted[frames[i][0]]['time'] = str(frames[i][1])

            sentences = []
            for j in range(2, len(frames[i])): # append text to the json data
                sentences.append(frames[i][j].split(" "))
            self.interpreted[str(frames[i][0])]['lines'] = sentences
        return self.interpreted

    def translate(self):
        interpreted = self.interpreted
        self.translated = interpreted
        sentence = ""
        lines = json.loads('{}') # save the amount of words of the lines in different frames in a json-string

        for i in range(0, len(interpreted)): # frame
            try: lines[str(i + 1)]
            except: lines[str(i + 1)] = {}

            for j in range(0, len(interpreted[str(i + 1)]['lines'])): # lines

                try: lines[str(i + 1)]
                except: lines[str(i + 1)] = {}

                sentence = sentence + self.buildstring(interpreted[str(i + 1)]['lines'][j], " ")
                try:
                    lines[str(i + 1)][str(j)] = len(interpreted[str(i + 1)]['lines'][j])
                except Exception: pass

                if sentence[-1] in ".!?" and not sentence[-2] in ".!?": # end of a sentence at the end of a line found
                    thread = threading.Thread(target=self.translation_executor, args=((sentence, lines),))
                    thread.start()
                    time.sleep(self.threadtime) # change this to a higher value if you get a "TranslationError DeepL call resulted in a unknown result." and wait some time to retry.
                    if i == len(interpreted) + 1:
                        thread.join()
                    sentence = ""
                    lines = json.loads('{}')

    def translation_executor(self, datatuple):
        sentence = datatuple[0]
        lines = datatuple[1]
        sentence = deepl.translate(sentence, self.tolang, self.fromlang).split(" ") # translate the sentence

        print(self.buildstring(sentence, " ")[1:])
        totalframes = len(lines)
        framecounter = 0

        for i in range(0, len(sentence)): # add buffer to prevent errors
            sentence.append([])

        for i in lines:  # frames
            framecounter += 1

            tallest_key = -1
            for j in lines[i]:
                if int(j) > tallest_key:
                    tallest_key = int(j)

            for j in lines[i]: # line
                wordamount = lines[i][j]

                if framecounter == totalframes and int(j) == tallest_key:  # last line of the translated section
                    newline = sentence
                else:  # not the last
                    newline = sentence[:wordamount]
                    sentence = sentence[wordamount:]

                self.translated[i]['lines'][int(j)] = []
                for k in range(0, len(newline)): # replace the original sentence with the translated sentence
                    if newline[k] != []:
                        self.translated[i]['lines'][int(j)].append(newline[k])
                if len(self.translated[i]['lines'][int(j)]) == 0: # prevent errors, if the translated is shorter than the original sentence
                    self.translated[i]['lines'][int(j)] = " "
                newline = []

    def buildfile(self):
        content = self.translated # create the file
        newfilename = self.buildstring(self.file.split(".")[:-1], "") + "_" + self.tolang.upper() + ".srt"
        try: os.remove(self.dir + newfilename)
        except: pass

        f = open(self.dir + newfilename, 'w')
        for i in range(0,len(content)):
            f.write(str(i + 1) + "\n")
            f.write(content[str(i + 1)]['time'] + "\n")

            for j in range(0, len(content[str(i + 1)]['lines'])):

                text = self.buildstring(content[str(i + 1)]['lines'][j], " ")[1:]
                #text = text.encode('cp850','replace').decode('cp850')
                f.write(text + "\n")

            if not i == len(content) - 1: # two free lines at the end of a file could cause errors
                f.write("\n")
        f.close()

    def run(self):
        good, error = self._check()
        if not good: #izzzz nisch gut
            return error
        self.readfile()
        self.interprete()
        print(json.dumps(self.interpreted, indent=4))
        self.translate()
        self.buildfile()

if __name__ == "__main__":
    tl = Translator()
    print(tl)
    tl.run()
