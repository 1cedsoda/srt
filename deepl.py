# python 3.6
import json
import os
import pydeepl as deepl  # https://github.com/EmilioK97/pydeepl/blob/master/pydeepl/pydeepl.py
import random
import platform
import re


def htmlsplit(string):
    splitten = []
    for i in range(0, len(string)):
        if string[i] == "<":
            splitten.append("<")
        elif string[i] == ">":
            splitten[len(splitten) - 1] = splitten[len(splitten) - 1] + ">"
            if i != len(string) - 1:
                splitten.append("")
        else:
            splitten[len(splitten) - 1] = splitten[len(splitten) - 1] + string[i]
    print(splitten)
    return splitten

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
        if dir == None:
            self.autodir()

        # define file and automaticly fill if possible
        if file == None:
            self.autofile()

        # define other
        self.interpreted = ""
        self.translated = ""
        self.builded = ""
        self.tolang = "DE"  # available languages aliases at line 6 to 13 at github.com/EmilioK97/pydeepl/blob/master/pydeepl/pydeepl.py
        self.fromlang = "auto"
        self.languges = ['DE', 'EN', 'FR', 'ES', 'IT', 'NL', 'PL']
        self.sentence = ["I'm a translation ", " bot for ssubtitle files!"]
        self.markers = []

    def __repr__(self):
        return str(self.dir + self.file)

    def setdir(self, dir):
        try:
            os.listdir(dir)
            self.dir = dir
            return True
        except Exception:
            return False

    def setfile(self, file):
        pass

    def _check(self):
        try:
            os.listdir(self.dir)
            try:
                open(self.dir + self.file, "r")
                return True
            except Exception:
                return False
        except Exception:
            return False

    def __markergen(self):
        chars = ['$', '%', '&', '/', '{', '}', '[', ']', ')', '=', '\\', '`', '*', '+', "'", '#']

        markers = []
        while len(markers) !=2:
            valid = False
            while not valid:
                marker = ""

                for i in range(0, 3):
                    char = chars[random.randint(0, len(chars) - 1)]
                    marker = marker + char
                translation = deepl.translate(self.sentence[0] + marker + self.sentence[1], self.tolang, self.fromlang)

                # count and analyse chars to know it chars of the marker are conteine zero or multiple times.
                countlist = '{}'
                countlist = json.loads(countlist)
                countvalid = True
                for i in range(0, len(chars)):
                    countlist[chars[i]] = 0
                for i in range(0, len(translation)):
                    try:
                        countlist[translation[i]] = countlist[translation[i]] + 1
                    except:
                        pass
                for i in range(0, len(marker)):
                    if countlist[marker[i]] != 1:
                        countvalid = False

                # search in the translation for the marker
                markervalid = False
                for i in range(0, len(translation)):
                    try:
                        if translation[i - 3:i] == marker:
                            markervalid = True
                    except:
                        pass

                if countvalid and markervalid:
                    valid = True
            markers.append(marker)
        self.markers = markers
        return markers

    def __interprete(self, directory=None, file=None):
        # 0
        if directory == None:
            directory = self.dir
        if file == None:
            file = self.file

        # 1 import file content
        filename = open(directory + file, "r", encoding='utf-8')
        content = filename.readlines()
        filename.close()
        for i in range(0, len(content)):  # remove BOM
            content[i] = content[i].replace('\ufeff', "")

        # 2 convert file to a list-structure
        frames = [[]]
        for i in range(0, len(content)):
            if content[i].rstrip() == "":  # create a new sublist, when there is a free line
                frames.append([])
            else:  # append content to the latest sublist
                frames[len(frames) - 1].append(content[i].rstrip())

        # 3 seperate frame declaration from the text
        seperated = json.loads('{"structure" : {}, "sentences" : []}')
        sentences = ["."]
        for i in range(0, len(frames)):
            current_frame = frames[i]
            seperated['structure'][current_frame[0]] = {}
            seperated['structure'][current_frame[0]]['time'] = current_frame[1]
            seperated['structure'][current_frame[0]]['lines'] = str(len(current_frame) - 2)
            seperated['structure'][current_frame[0]]['wordsperline'] = json.loads('{}')

            for j in range(2, len(frames[i])):

                last_char = sentences[-1][-1]
                text = frames[i][j].rstrip()
                words = len(text.split(" "))
                seperated['structure'][current_frame[0]]['wordsperline'][str(j-2)] = words
                if last_char in ".!?":  # new sentence
                    sentences.append(text)
                else:
                    if j > 2:  # not the first line of a frame
                        sentences[-1] = sentences[-1] +  text
                    else:  # first line of a frame
                        sentences[-1] = sentences[-1] + text
            sentences[-1] = sentences[-1][:-1] + sentences[-1][-1]

        seperated['sentences'] = sentences[1:]
        self.interpreted = seperated
        return seperated

    def __translate(self, showstatus):
        translated = self.interpreted
        lenght = len(translated['sentences'])-1
        for i in range(0, len(translated['sentences'])):

                sentence = translated['sentences'][i]
                htmlsplitten = htmlsplit(sentence)
                for j in range(0, len(htmlsplitten)):
                    if htmlsplitten[i][0] != "<":
                        print(htmlsplitten[j])
                        translation = deepl.translate(htmlsplitten[j], self.tolang, self.fromlang)
                        htmlsplitten[i] = translation
                        translated['sentences'][i] = translation

                if showstatus:
                    try: print("Translation " + str(100/lenght*i) + "%", end="\r")
                    except Exception: pass
        self.translated = translated

    def __buildfile(self, export=False):
        frames = []
        for i in range(0, len(self.translated['structure'])):
            for j in range(0, int(self.translated['structure'][str(i + 1)]['sentences'])):
                pass
        return True

    def run(self):
        if not self._check():
            return False
        #self.__markergen()
        #print(self.markers)
        self.__interprete()
        print("Interpreted")
        #print(self.interpreted)
        self.__translate(True)
        print("Translated")
        # self.__buildfile()
        return self.translated

if __name__ == "__main__":
    tl = Translator()
    tl.file = "aaa.srt"
    something = tl.run()
    print(json.dumps(tl.translated, sort_keys=True, indent=4))
    input()