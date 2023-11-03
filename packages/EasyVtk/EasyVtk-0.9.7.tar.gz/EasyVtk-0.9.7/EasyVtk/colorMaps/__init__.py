from os import listdir, getcwd
from os.path import isfile
from json import load
from . import ColorMap

colorMaps = dict()
colorMapsNames = list()

path = getcwd() + '\\EasyVtk\\colorMaps'
for filename in listdir(path):
    filename = f'{path}\\{filename}'
    if isfile(filename) and filename.endswith('.json'):
        with open(filename) as file:
            data = load(file)[0]
            if all(key in data for key in ('Name', 'RGBPoints')):
                name = data['Name']
                if name not in colorMaps:
                    colorMaps[name] = data['RGBPoints']
                else:
                    print(f'Color map "{name}" already exists ({filename})')
                colorMapsNames.append(name)

colorMapsNames = tuple(colorMapsNames)
