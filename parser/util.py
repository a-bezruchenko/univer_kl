import aiofiles
# этот файл содержит вспомогательные функции

# Убирает формат и ставит вместо него png
def convertNameToPng(image_name):
    replaceAfter(image_name, '.', 'png')

def replaceAfter(string:str, symbol:str, replace_with:str):
    i = 0
    while(string[-i]!=symbol):
        i+=1
    return string[:-i+1] + replace_with

# Вычленяет расширение картинки из её url
def getExtention(url):
    return getLastFrom(url, '.')

# Вычленяет имя картинки из её url
def getName(url):
    return getLastFrom(url, '/')

# Выдаёт подстроку после последнего вхождения данного символа
def getLastFrom(string:str, symbol: str):
    i = len(string) - 1
    while(string[i]!=symbol):
        i-=1
    return string[i+1:]

# Обрезает подстроку после последнего вхождения данного символа
def cutLastFrom(string:str, symbol: str):
    i = len(string) - 1
    while(string[i]!=symbol):
        i-=1
    return string[:i]

def readFile(filename):
    res = []
    with open(filename, "r") as f:
        for line in f:
            res.append(line)
    return res

async def append_to_file(arr, filename: str):
    async with aiofiles.open(filename, "a") as f:
        for e in arr:
            await f.write(e + '\n')

def intTryParse(value, defaultVal):
    try:
        return int(value)
    except ValueError:
        return defaultVal

def tryFunction(function, defaultVal, params={}):
    try:
        return function(*params)
    except Exception:
        return defaultVal