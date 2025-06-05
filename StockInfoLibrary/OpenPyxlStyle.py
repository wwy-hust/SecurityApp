# -*- coding:utf-8 -*-
from openpyxl.styles import Alignment, PatternFill, Color, numbers
from openpyxl.formatting.rule import Rule, DataBarRule, ColorScaleRule, ColorScale, FormatObject, IconSet
from openpyxl.formatting.formatting import ConditionalFormattingList

def GetVolatilityIconSetRule():
    first = FormatObject(type='num', val=1.3)
    second = FormatObject(type='num', val=2.5)
    third = FormatObject(type='num', val=5.0)
    forth = FormatObject(type='num', val=10.0)

    iconset = IconSet(iconSet='4TrafficLights', cfvo=[second, first, third, forth], showValue=None, percent=None, reverse=True)
    IconSetRule = Rule(type='iconSet', iconSet=iconset)
    return IconSetRule