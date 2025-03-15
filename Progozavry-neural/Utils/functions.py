import os

def toASCII(name, idx, channel):
    filename = os.path.abspath('../' + name + f'/Nr {idx}/N-{idx}.REC')
    pathRes = os.path.abspath('../data')
    res = []
    if os.path.isfile(filename):
        if not os.path.isdir('../data'):
            os.mkdir('../data')
        temp = f'{name}_{idx}_{channel}'
        if not os.path.isfile(f'{pathRes}/{temp}.txt'):
            os.system(f'.\..\Programs\EDFtoASCII\EDFToASCII.exe "{filename}" {channel} "{pathRes}/{temp}.txt" "{pathRes}/{temp}.ascii" /BATCH')
        with open(f'{pathRes}/{temp}.ascii') as f:
            for line in f.readlines():
                res.append(float(line.strip()))
        #os.remove(f'{pathRes}/{temp}.txt')
        #os.remove(f'{pathRes}/{temp}.ascii')
    else:
        print(f"file {filename} nit exist")
    return res



