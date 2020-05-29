# coding: utf8
# этот файл содержит вспомогательные функции
import aiofiles

def replaceAfter(string:str, symbol:str, replace_with:str):
    i = 0
    while(string[-i]!=symbol):
        i+=1
    return string[:-i+1] + replace_with

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