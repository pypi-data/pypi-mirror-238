from . import commonFunctions
from . import commonClasses


pvd = {
    'time': '0'
}

cut = {
    'normal': ('0', '0', '1')
}

isoline = {
    'showLabels': False,
    'numberOfLines': '10',
    'isolineColor': (1, 1, 1),
    'labelColor': (0, 0, 0)
}

clip = {
    'invert': False,
    'normal': ('0', '0', '1')
}


threshold = {
    'invert': False
}


TypeToString = {
    commonClasses.Type.pvd: 'PVD',
    commonClasses.Type.cut: 'Cut',
    commonClasses.Type.isoline: 'Isoline',
    commonClasses.Type.clip: 'Clip',
    commonClasses.Type.threshold: 'Threshold',
    commonClasses.Type.calculator: 'Calculator',
    commonClasses.Type.outline: 'Outline',
    commonClasses.Type.another: 'Another'
}

creation_permission = {
    commonClasses.Type.pvd: [],
    commonClasses.Type.cut: [commonClasses.Type.pvd, commonClasses.Type.clip, commonClasses.Type.threshold],
    commonClasses.Type.isoline: [commonClasses.Type.cut],
    commonClasses.Type.clip: [commonClasses.Type.pvd, commonClasses.Type.clip, commonClasses.Type.threshold],
    commonClasses.Type.threshold: [commonClasses.Type.pvd, commonClasses.Type.clip, commonClasses.Type.threshold, commonClasses.Type.cut],
    commonClasses.Type.calculator: [commonClasses.Type.pvd],
    commonClasses.Type.outline: [commonClasses.Type.pvd, commonClasses.Type.cut, commonClasses.Type.clip, commonClasses.Type.threshold]
}
