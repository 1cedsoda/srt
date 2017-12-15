# python 3.6
import json
import os
import platform
import pydeepl as deepl  # https://github.com/EmilioK97/pydeepl/blob/master/pydeepl/pydeepl.py
import random
import re


def splithtml(string):
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

def removehtml(content):
    if not content is list:
        content = splithtml(content)
    string = ""
    if len(content) != 0:
        for i in range(0, len(content)):
            try:
                if not content[i][0] == "<":
                    string += content[i]
            except Exception: pass
        return string
    else:
        return content

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
        self.translated = '{"sentences": ["Hal","Ich bin es, Ember, Gott von Fillory.","Verbeugen Sie sich und kriechen Sie. Ich warte.","Oh, aber ich habe dir so viel zu erz\u00e4hlen.","Ich, mit kleiner Hilfe von Mybrother Umber.... R.I.P......","erschuf eine filigrane Welt, und so nannte ich sie, au\u00dfer, dass ich ein bisschen betrunken war, also... Fillory.","Ein mit Magie vollgestopftes St\u00fcck, geschw\u00e4tzigen Tieren, sexy Kreaturen.","Wirklich, was f\u00fcr ein Planet.","Ich kalibrierte alles f\u00fcr maximale Unterhaltung.","Ich ordnete an, dass es von den Kindern der Erde regiert wird, ein m\u00fcrrischer kleiner Planet, der f\u00fcr seine tapferen Zauberer bekannt ist.","Diese tapferen Seelen w\u00fcrden kommen, und wenn sie langweilig wurden, gingen sie weg.","Ein typisches Beispiel daf\u00fcr ist Martin Chatwin.","Tapferer, kluger Junge, geborener Held, aber ehrlich, sehr unangenehm zu beobachten, dass er bel\u00e4stigt wurde.","Also habe ich die schwierige Entscheidung getroffen, ihn rauszuwerfen und ihn durch jemanden zu ersetzen, der schlagkr\u00e4ftiger und lustiger ist, aber Martin war hartn\u00e4ckiger als ich ihm zugeschrieben habe.","Er trank von der Wellspring, um stark zu werden, und schraubte dabei Fillory,"    ],    "structure": {"1": {    "lines": "1",    "time": "00:00:00,251 --> 00:00:02,293",    "wordsperline": {"0": 3    }},"10": {    "lines": "1",    "time": "00:00:23,307 --> 00:00:24,406",    "wordsperline": {"0": 2    }},"11": {    "lines": "1",    "time": "00:00:24,442 --> 00:00:25,441",    "wordsperline": {"0": 2    }},"12": {    "lines": "1",    "time": "00:00:25,476 --> 00:00:27,543",    "wordsperline": {"0": 4    }},"13": {    "lines": "2",    "time": "00:00:27,578 --> 00:00:30,779",    "wordsperline": {"0": 3,"1": 3    }},"14": {    "lines": "2",    "time": "00:00:30,815 --> 00:00:34,016",    "wordsperline": {"0": 5,"1": 4    }},"15": {    "lines": "2",    "time": "00:00:34,051 --> 00:00:36,719",    "wordsperline": {"0": 5,"1": 4    }},"16": {    "lines": "1",    "time": "00:00:36,754 --> 00:00:38,687",    "wordsperline": {"0": 5    }},"17": {    "lines": "1",    "time": "00:00:38,723 --> 00:00:40,589",    "wordsperline": {"0": 8    }},"18": {    "lines": "1",    "time": "00:00:40,624 --> 00:00:42,858",    "wordsperline": {"0": 5    }},"19": {    "lines": "1",    "time": "00:00:42,893 --> 00:00:45,494",    "wordsperline": {"0": 5    }},"2": {    "lines": "1",    "time": "00:00:02,293 --> 00:00:04,787",    "wordsperline": {"0": 7    }},"20": {    "lines": "2",    "time": "00:00:45,529 --> 00:00:48,364",    "wordsperline": {"0": 2,"1": 4    }},"21": {            "lines": "1",            "time": "00:00:48,399 --> 00:00:49,698",            "wordsperline": {                "0": 4            }        },        "22": {            "lines": "1",            "time": "00:00:49,734 --> 00:00:51,700",            "wordsperline": {                "0": 6            }        },        "23": {            "lines": "1",            "time": "00:00:51,736 --> 00:00:53,035",            "wordsperline": {                "0": 7            }        },        "24": {            "lines": "1",            "time": "00:00:53,070 --> 00:00:55,404",            "wordsperline": {                "0": 6            }        },        "25": {            "lines": "2",            "time": "00:00:55,439 --> 00:00:58,741",            "wordsperline": {                "0": 5,                "1": 6            }        },        "26": {            "lines": "2",            "time": "00:00:58,776 --> 00:01:00,876",            "wordsperline": {                "0": 4,                "1": 4            }        },        "27": {            "lines": "1",            "time": "00:01:00,911 --> 00:01:02,978",            "wordsperline": {                "0": 5            }        },        "3": {            "lines": "1",            "time": "00:00:04,822 --> 00:00:07,222",            "wordsperline": {                "0": 8            }        },        "4": {            "lines": "1",            "time": "00:00:07,258 --> 00:00:09,325",            "wordsperline": {                "0": 9            }        },        "5": {            "lines": "2",            "time": "00:00:09,360 --> 00:00:12,528",            "wordsperline": {                "0": 6,                "1": 3            }        },        "6": {            "lines": "1",            "time": "00:00:12,563 --> 00:00:15,964",            "wordsperline": {                "0": 6            }        },        "7": {            "lines": "1",            "time": "00:00:16,000 --> 00:00:18,334",            "wordsperline": {                "0": 7            }        },        "8": {            "lines": "1",            "time": "00:00:18,369 --> 00:00:21,437",            "wordsperline": {                "0": 8            }        },        "9": {            "lines": "1",            "time": "00:00:21,472 --> 00:00:23,272",            "wordsperline": {                "0": 4            }        }    }}'
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
        for i in range(0, len(content)):
            content[i] = removehtml(content[i].rstrip())

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
                translation = deepl.translate(sentence, self.tolang, self.fromlang)
                translated['sentences'][i] = translation

                if showstatus:
                    print("")
                    print("EN:", sentence)
                    print("DE:", translation)
                    try: print("Translation " + str(float(int(100/lenght*i*10)/10)) + "%", end="\n")
                    except Exception: pass
        self.translated = translated

    def __buildfile(self, export=False):
        frames = []
        for i in range(0, len(self.translated['structure'])):
            frames.append([])
            last = len(frames) - 1
            frames[last].append(str(i + 1))
            frames[last].append(self.translated['structure'][str(i + 1)]['time'])

            for j in range(0, int(len(self.translated['structure'][str(i + 1)]['wordsperline']))):
                wordsperline = self.translated['structure'][str(i + 1)]['wordsperline'][str(j)]
                last_sentence = self.translated['sentences'][0].split(" ")
                for k in range(0, 1):
                    k = k - 1
                    try:
                        if last_sentence[wordsperline + k][-1] in ".!?":
                            print(wordsperline + k + 1)
                            frames[last].append(str(self.translated['sentences'][0][:wordsperline + k + 1]))
                            print(self.translated['sentences'][0][:wordsperline + k + 1])
                            self.translated['sentences'][0] = self.translated['sentences'][0][:wordsperline + k + 1]
                    except Exception as e:
                        #raise e
                        #pass
                        print(e)
        return frames

    def run(self):
        if not self._check():
            return False
        #self.__markergen()
        #print(self.markers)
        #self.__interprete()
        #print("Interpreted")
        #print(self.interpreted)
        #self.__translate(True)
        #print("Translated")
        #self.translated = self.interpreted
        return self.__buildfile()

if __name__ == "__main__":
    tl = Translator()
    tl.file = "aaa.srt"
    something = tl.run()
    print(json.dumps(tl.translated, sort_keys=True, indent=4))
    input()
