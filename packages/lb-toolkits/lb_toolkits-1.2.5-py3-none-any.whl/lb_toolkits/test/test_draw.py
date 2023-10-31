# -*- coding:utf-8 -*-
'''
@Project     : lb_toolkits

@File        : test_draw.py

@Modify Time :  2022/11/10 14:49   

@Author      : Lee    

@Version     : 1.0   

@Description :

'''
import os
import sys
import numpy as np
import datetime

from lb_toolkits.draw import GetColorList,colorbar

from qgis.core import *
from PyQt5.Qt import *
import copy
import os.path
import qgis_util_mm
import settings


def modify_labeling_river(project, label_para, font_dpi=96):
    """
    修改河流字体、线段的样式。
    :param project: 工程对象
    :param label_para: 河流字体、线段的样式参数
    :param font_dpi: 布局dpi，px转化为mm时需要，默认96
    :return: None
    """

    # for name in ['NAME_SEA']:
    #     if name in layer_names:
    #         label_layer = project.mapLayersByName(name)[0]
    # if not label_layer:
    #     print(f'无river图层')
    #     return

    if not label_para:
        label_para = {'fontColor': '#0a7899', 'fontFamily': '微软雅黑', 'fontSize': 10, 'fontStyle': 'normal',
                      'lineColor': '#11BAEE', 'lineSize': '1', 'lineStyle': '实线'}

    # 字体属性
    layer_names = [layer.name() for layer in list(project.mapLayers().values())]
    for river_name in ['NAME_SEA', 'NAME_L2', 'NAME_L3']:
        if river_name in layer_names:
            label_layer = project.mapLayersByName(river_name)[0]
        else:
            print(f'无{river_name}图层！')
            continue
        label = label_layer.labeling()
        label_settings = label.rootRule().children()[0].settings()
        text_format = label_settings.format()
        font_family = '微软雅黑' if 'fontFamily' not in label_para else label_para['fontFamily']
        font = QFont(font_family)
        if 'fontStyle' in label_para:
            if label_para['fontStyle'] == 'underline':
                font.setUnderline(True)
            if label_para['fontStyle'] == 'bold':
                font.setBold(True)
            if label_para['fontStyle'] == 'italic':
                font.setItalic(True)
        text_format.setFont(font)
        font_size = 10 if 'fontSize' not in label_para else label_para['fontSize']
        text_format.setSize(font_size / font_dpi * 72)
        text_format.setSizeUnit(QgsUnitTypes.RenderPoints)
        font_color = '#0A7899' if 'fontColor' not in label_para else label_para['fontColor']
        text_format.setColor(QColor(font_color))
        label_settings.setFormat(text_format)
        for k in label_settings.dataDefinedProperties().propertyKeys():
            # prop = label_settings.dataDefinedProperties().property(k)
            # if 'case when @map_scale>20000000' in prop.asExpression():
            #     prop.setExpressionString('case when @map_scale>35000000 then 7 end')
            if k == QgsPalLayerSettings.Size:
                prop = label_settings.dataDefinedProperties().property(k)
                prop.setExpressionString('case when @map_scale>35000000 then 7 end')
        label.setSettings(label_settings)

    # 界线属性
    for river_line in ['RIVER_L2', 'RIVER_L3', 'PHYDL_china', 'PHYDL_2']:
        if river_line in layer_names:
            line_layer = project.mapLayersByName(river_line)[0]
        else:
            print(f'无{river_line}图层！')
            continue
        line = line_layer.renderer()
        line_symbol = line.rootRule().children()[0].symbol()
        # 界线颜色
        line_color = '#11BAEE' if 'lineColor' not in label_para else label_para['lineColor']
        line_symbol.setColor(QColor(line_color))
        # 界线宽度 1默认 2加粗 3无
        if 'lineSize' in label_para:
            if str(label_para['lineSize']) == '2':
                line_symbol.symbolLayer(0).setWidth(line_symbol.symbolLayer(0).width() * 2)
            elif str(label_para['lineSize']) == '3':
                line_symbol.symbolLayer(0).setEnabled(False)
        # 界线虚实
        if 'lineStyle' in label_para and label_para['lineStyle'] == '虚线':
            line_symbol.symbolLayer(0).setUseCustomDashPattern(True)
            line_symbol.symbolLayer(0).setCustomDashVector((0.8, 1.6))
            line_symbol.symbolLayer(0).setCustomDashPatternUnit(QgsUnitTypes.RenderMillimeters)


def modify_line_prop(line_layer, label_para, area, line_name=''):
    line = line_layer.renderer()
    for i, line_rule in enumerate(line.rootRule().children()):
        line_symbol = line_rule.symbol()
        # 界线宽度
        if 'lineSize' in label_para:
            if area in ['railroads', 'roads_guodao', 'roads_shengdao']:
                if str(label_para['lineSize']) == '-1':
                    # line_symbol.symbolLayer(0).setEnabled(False)
                    line_rule.setActive(False)
                else:
                    line_symbol.symbolLayer(0).setWidth(float(label_para['lineSize']))
            else:
                if str(label_para['lineSize']) == '2':  # 1默认 2加粗 3无
                    if area == 'prov':
                        old_vector = line_symbol.symbolLayer(0).dxfCustomDashPattern()
                        # print(f'old_vector: {old_vector}')
                        if not old_vector or not old_vector[0]:
                            continue
                        if i == 0:
                            new_vector = (old_vector[0][0], old_vector[0][1] * 3)
                        else:
                            new_vector = (old_vector[0][0], old_vector[0][1] * 3, old_vector[0][2], old_vector[0][3] * 3)
                        line_symbol.symbolLayer(0).setCustomDashVector(new_vector)
                        line_symbol.symbolLayer(0).setCustomDashPatternUnit(old_vector[1])
                        line_symbol.symbolLayer(0).setWidth(line_symbol.symbolLayer(0).width() * 2)
                        # print('new_vector: ', line_symbol.symbolLayer(0).dxfCustomDashPattern())
                    elif area in ['city', 'county']:
                        line_symbol.symbolLayer(0).setWidth(line_symbol.symbolLayer(0).width() * 3)
                elif str(label_para['lineSize']) == '3':
                    # line_symbol.symbolLayer(0).setEnabled(False)
                    line_rule.setActive(False)
        # 界线颜色
        line_color = '#000000' if 'lineColor' not in label_para else label_para['lineColor']
        if line_name == 'RailRoads':
            line_symbol.symbolLayer(0).setColor(QColor(line_color))
        else:
            line_symbol.setColor(QColor(line_color))
        # 界线虚实
        if 'lineStyle' in label_para and label_para['lineStyle'] == '实线':
            if isinstance(line_symbol.symbolLayer(0), QgsSimpleLineSymbolLayer):
                line_symbol.symbolLayer(0).setUseCustomDashPattern(False)


def modify_labeling(project, label_para, area, server_type, layout_dpi=96, font_dpi=96):
    """
    修改省、市、县的字体、界线、符号的样式。
    :param project: 工程对象
    :param label_para: 字体、界线、符号的样式参数
    :param area: 省、市、县标识
    :param server_type: 前端页面样式类型
    :param layout_dpi: 布局dpi，px转化为mm时需要，默认96
    :param font_dpi: 字体pi，px转化为pt时需要，默认34
    :return: None
    """

    layer_names = [layer.name() for layer in list(project.mapLayers().values())]

    label_layer = None
    if area == 'prov':
        for label_name in ['AGNP_SHCS', 'AGNP_SHCS1']:
            if label_name in layer_names:
                label_layer = project.mapLayersByName(label_name)[0]
    elif area == 'city':
        for label_name in ['AGNP_D1']:
            if label_name in layer_names:
                label_layer = project.mapLayersByName(label_name)[0]
    elif area == 'county':
        for label_name in ['AGNP_X1']:
            if label_name in layer_names:
                label_layer = project.mapLayersByName(label_name)[0]
    elif area == 'beijing':
        for label_name in ['SD']:
            if label_name in layer_names:
                label_layer = project.mapLayersByName(label_name)[0]
    elif area == 'railroads':
        for label_name in ['RailRoads']:
            if label_name in layer_names:
                label_layer = project.mapLayersByName(label_name)[0]
    elif area == 'roads_guodao':
        for label_name in ['main_road_mark']:
            if label_name in layer_names:
                label_layer = project.mapLayersByName(label_name)[0]
    elif area == 'roads_shengdao':
        for label_name in ['all_road_mark']:
            if label_name in layer_names:
                label_layer = project.mapLayersByName(label_name)[0]
    if not label_layer:
        print(f'无{area}图层！')
        return

    if not label_para:
        if area == 'prov':
            if server_type == 'rp0':
                label_para = {'fontColor': '#000000', 'fontFamily': '微软雅黑', 'fontSize': 11, 'fontStyle': 'normal',
                              'lineColor': '#000000', 'lineSize': '1', 'lineStyle': '虚线', 'markColor': '#000000',
                              'markSize1': '5', 'markSize2': '1'}
            elif server_type == 'rp1':
                label_para = {'fontColor': '#000000', 'fontFamily': '微软雅黑', 'fontSize': 20, 'fontStyle': 'normal',
                              'lineColor': '#000000', 'lineSize': '1', 'lineStyle': '虚线', 'markColor': '#000000',
                              'markSize1': '5', 'markSize2': '1'}
            elif server_type == 'rp2':
                label_para = {'fontColor': '#000000', 'fontFamily': '微软雅黑', 'fontSize': 20, 'fontStyle': 'normal',
                              'lineColor': '#000000', 'lineSize': '1', 'lineStyle': '虚线', 'markColor': '#000000',
                              'markSize1': '5', 'markSize2': '1'}
            else:
                label_para = {'fontColor': '#000000', 'fontFamily': '微软雅黑', 'fontSize': 12, 'fontStyle': 'normal',
                              'lineColor': '#000000', 'lineSize': '1', 'lineStyle': '虚线', 'markColor': '#000000',
                              'markSize1': '5', 'markSize2': '1'}
        elif area == 'city':
            if server_type == 'rp0':
                label_para = {'fontColor': '#000000', 'fontFamily': '黑体', 'fontSize': 16, 'fontStyle': 'normal',
                              'lineColor': '#000000', 'lineSize': '1', 'lineStyle': '虚线', 'markColor': '#000000',
                              'markSize1': '5'}
            elif server_type == 'rp1':
                label_para = {'fontColor': '#000000', 'fontFamily': '黑体', 'fontSize': 14, 'fontStyle': 'normal',
                              'lineColor': '#000000', 'lineSize': '1', 'lineStyle': '虚线', 'markColor': '#000000',
                              'markSize1': '5'}
            elif server_type == 'rp2':
                label_para = {'fontColor': '#000000', 'fontFamily': '黑体', 'fontSize': 14, 'fontStyle': 'normal',
                              'lineColor': '#000000', 'lineSize': '1', 'lineStyle': '虚线', 'markColor': '#000000',
                              'markSize1': '5'}
            else:
                label_para = {'fontColor': '#000000', 'fontFamily': '黑体', 'fontSize': 14, 'fontStyle': 'normal',
                              'lineColor': '#000000', 'lineSize': '1', 'lineStyle': '虚线', 'markColor': '#000000',
                              'markSize1': '5'}
        elif area == 'county':
            if server_type == 'rp0':
                label_para = {'fontColor': '#000000', 'fontFamily': '黑体', 'fontSize': 14, 'fontStyle': 'normal',
                              'lineColor': '#000000', 'lineSize': '1', 'lineStyle': '虚线', 'markColor': '#000000',
                              'markSize1': '6'}
            elif server_type == 'rp1':
                label_para = {'fontColor': '#000000', 'fontFamily': '黑体', 'fontSize': 14, 'fontStyle': 'normal',
                              'lineColor': '#000000', 'lineSize': '1', 'lineStyle': '虚线', 'markColor': '#000000',
                              'markSize1': '6'}
            elif server_type == 'rp2':
                label_para = {'fontColor': '#000000', 'fontFamily': '黑体', 'fontSize': 14, 'fontStyle': 'normal',
                              'lineColor': '#000000', 'lineSize': '1', 'lineStyle': '虚线', 'markColor': '#000000',
                              'markSize1': '6'}
            else:
                label_para = {'fontColor': '#000000', 'fontFamily': '黑体', 'fontSize': 12, 'fontStyle': 'normal',
                              'lineColor': '#000000', 'lineSize': '1', 'lineStyle': '虚线', 'markColor': '#000000',
                              'markSize1': '6'}
        elif area == 'beijing':
            if server_type == 'rp0':
                label_para = {'fontColor': '#000000', 'fontFamily': '微软雅黑', 'fontSize': 13, 'fontStyle': 'normal',
                              'markColor': '#FF0000', 'markSize1': '4', 'markSize2': '7'}
            elif server_type == 'rp1':
                label_para = {'fontColor': '#000000', 'fontFamily': '微软雅黑', 'fontSize': 22, 'fontStyle': 'normal',
                              'markColor': '#FF0000', 'markSize1': '4', 'markSize2': '7'}
            elif server_type == 'rp2':
                label_para = {'fontColor': '#000000', 'fontFamily': '微软雅黑', 'fontSize': 22, 'fontStyle': 'normal',
                              'markColor': '#FF0000', 'markSize1': '4', 'markSize2': '7'}
            else:
                label_para = {'fontColor': '#000000', 'fontFamily': '微软雅黑', 'fontSize': 14, 'fontStyle': 'normal',
                              'markColor': '#FF0000', 'markSize1': '4', 'markSize2': '7'}
    else:
        if area == 'beijing':
            label_para['markSize1'], label_para['markSize2'] = label_para['markSize2'], label_para['markSize1']

    # 字体属性
    label = label_layer.labeling()
    for label_rule in label.rootRule().children():
        label_settings = label_rule.settings()
        text_format = label_settings.format()
        QgsPalLayerSettings()
        font_family = '微软雅黑' if 'fontFamily' not in label_para else label_para['fontFamily']
        font = QFont(font_family)
        if 'fontStyle' in label_para:
            if label_para['fontStyle'] == 'underline':
                font.setUnderline(True)
            if label_para['fontStyle'] == 'bold':
                font.setBold(True)
            if label_para['fontStyle'] == 'italic':
                font.setItalic(True)
        text_format.setFont(font)
        font_size = 14 if 'fontSize' not in label_para else label_para['fontSize']
        text_format.setSize(font_size / font_dpi * 72)
        text_format.setSizeUnit(QgsUnitTypes.RenderPoints)
        font_color = '#000000' if 'fontColor' not in label_para else label_para['fontColor']
        text_format.setColor(QColor(font_color))
        label_settings.setFormat(text_format)
        # if area == 'prov':
        # for k in label_settings.dataDefinedProperties().propertyKeys():
        # print('>'*20, label_settings.dataDefinedProperties().property(k).expressionString())
        # if k == QgsPalLayerSettings.Size:
        #     prop = label_settings.dataDefinedProperties().property(k)
        #     prop.setExpressionString('case when @map_scale>35000000 then 6 end')
        # prop = label_settings.dataDefinedProperties().property(k)
        # if 'case when @map_scale>' in prop.asExpression():
        #     # prop.setActive(False)
        #     prop.setExpressionString('case when @map_scale>35000000 then 6 end')
        # print('>'*20, label_settings.dataDefinedProperties().property(k).expressionString())
        # label_rule.setSettings(label_settings)
        # for k, v in QgsPalLayerSettings.propertyDefinitions().items():
        #     print(k, v.name())
        # 0 Size
        # 77 OffsetQuad
        # if area in ['city', 'county']:
        #     for k in label_settings.dataDefinedProperties().propertyKeys():
        #         if k == QgsPalLayerSettings.Size:
        #             prop = label_settings.dataDefinedProperties().property(k)
        #             prop.setExpressionString('"Value"')
        #     label_rule.setSettings(label_settings)

    # 符号属性
    if area in ['prov', 'city', 'county', 'beijing']:
        symbol = label_layer.renderer()
        for symbol_rule in symbol.rootRule().children():
            marker_symbols = symbol_rule.symbol()
            mark_size1 = 5 if 'markSize1' not in label_para else float(label_para['markSize1'])
            marker_symbols.symbolLayer(0).setSize(mark_size1 / layout_dpi * 25.4)
            marker_symbols.symbolLayer(0).setSizeUnit(QgsUnitTypes.RenderMillimeters)
            mark_color = '#000000' if 'markColor' not in label_para else label_para['markColor']
            marker_symbols.symbolLayer(0).setStrokeColor(QColor(mark_color))
            if area in ['prov', 'beijing']:
                marker_symbols.symbolLayer(0).dataDefinedProperties().clear()  # 删除设置的表达式
                marker_symbols.symbolLayer(1).dataDefinedProperties().clear()
                mark_size2 = 1 if 'markSize2' not in label_para else float(label_para['markSize2'])
                marker_symbols.symbolLayer(1).setSize(mark_size2 / layout_dpi * 25.4)
                marker_symbols.symbolLayer(1).setSizeUnit(QgsUnitTypes.RenderMillimeters)
                marker_symbols.symbolLayer(1).setStrokeColor(QColor(mark_color))
                if area == 'prov':
                    marker_symbols.symbolLayer(1).setFillColor(QColor(mark_color))

    # 界线属性
    if area == 'prov':
        for line_name in ['PROULN_SJ', 'PROULN_SJ_NEW', 'BOUA_S']:
            if line_name in layer_names:
                line_layer = project.mapLayersByName(line_name)[0]
                modify_line_prop(line_layer, label_para, area, line_name)
            else:
                print(f'无{area}图层！')
                continue
    elif area == 'city':
        for line_name in ['BOUA_D']:
            if line_name in layer_names:
                line_layer = project.mapLayersByName(line_name)[0]
                modify_line_prop(line_layer, label_para, area)
            else:
                print(f'无{area}图层！')
                continue
    elif area == 'county':
        for line_name in ['BOUA_X']:
            if line_name in layer_names:
                line_layer = project.mapLayersByName(line_name)[0]
                modify_line_prop(line_layer, label_para, area)
            else:
                print(f'无{area}图层！')
                continue
    elif area == 'railroads':
        for line_name in ['RailRoads']:
            if line_name in layer_names:
                line_layer = project.mapLayersByName(line_name)[0]
                modify_line_prop(line_layer, label_para, area, line_name)
            else:
                print(f'无{area}图层！')
                continue
    elif area == 'roads_guodao':
        for line_name in ['roa_ln_GuoDao']:
            if line_name in layer_names:
                line_layer = project.mapLayersByName(line_name)[0]
                modify_line_prop(line_layer, label_para, area)
            else:
                print(f'无{area}图层！')
                continue
    elif area == 'roads_shengdao':
        for line_name in ['roa_ln_ShengLu']:
            if line_name in layer_names:
                line_layer = project.mapLayersByName(line_name)[0]
                modify_line_prop(line_layer, label_para, area)
            else:
                print(f'无{area}图层！')
                continue


def show_city_county_river_labels_lines(project, city_para, county_para, river_para, railroads_para, roads_guodao_para,
                                        roads_shengdao_para):
    city_show = city_para['show'] if 'show' in city_para else False
    county_show = county_para['show'] if 'show' in county_para else False
    railroads_show = railroads_para['show'] if 'show' in railroads_para else False
    roads_guodao_show = roads_guodao_para['show'] if 'show' in roads_guodao_para else False
    roads_shengdao_show = roads_shengdao_para['show'] if 'show' in roads_shengdao_para else False
    if 'levelShow' in river_para:
        r1_show = True if '1' in river_para['levelShow'] else False
        r2_show = True if '2' in river_para['levelShow'] else False
        r3_show = True if '3' in river_para['levelShow'] else False
    else:
        r1_show, r2_show, r3_show = True, False, False
    # print('>'*20, f'county_show: {county_show}, county_show: {county_show}')

    layer_names = [layer.name() for layer in list(project.mapLayers().values())]

    # 设置省界显隐
    for prov_line_name in ['PROULN_SJ', 'PROULN_SJ_NEW']:
        if prov_line_name in layer_names:
            prov_line_layer = project.mapLayersByName(prov_line_name)[0]
            if city_show or county_show:
                prov_line_layer.renderer().rootRule().children()[0].symbol().symbolLayer(0).setEnabled(False)
                prov_line_layer.renderer().rootRule().children()[1].symbol().symbolLayer(0).setEnabled(True)
            else:
                prov_line_layer.renderer().rootRule().children()[0].symbol().symbolLayer(0).setEnabled(True)
                prov_line_layer.renderer().rootRule().children()[1].symbol().symbolLayer(0).setEnabled(False)
    for prov_line_name in ['BOUA_S']:
        if prov_line_name in layer_names:
            prov_line_layer = project.mapLayersByName(prov_line_name)[0]
            if city_show or county_show:
                prov_line_layer.renderer().rootRule().children()[0].symbol().symbolLayer(0).setEnabled(True)
            else:
                prov_line_layer.renderer().rootRule().children()[0].symbol().symbolLayer(0).setEnabled(False)

    # 设置市名、市界显隐
    for city_label_name in ['AGNP_D1']:
        if city_label_name in layer_names:
            city_label_layer = project.mapLayersByName(city_label_name)[0]
            for city_symbol_rule in city_label_layer.renderer().rootRule().children():
                city_symbol_rule.symbol().symbolLayer(0).setEnabled(city_show)
            for city_label_rule in city_label_layer.labeling().rootRule().children():
                city_label_rule.settings().drawLabels = city_show
    for city_line_name in ['BOUA_D']:
        if city_line_name in layer_names:
            city_line_layer = project.mapLayersByName(city_line_name)[0]
            if city_show:
                if county_show:
                    city_line_layer.renderer().rootRule().children()[0].symbol().symbolLayer(0).setEnabled(False)
                    city_line_layer.renderer().rootRule().children()[1].symbol().symbolLayer(0).setEnabled(True)
                else:
                    city_line_layer.renderer().rootRule().children()[0].symbol().symbolLayer(0).setEnabled(True)
                    city_line_layer.renderer().rootRule().children()[1].symbol().symbolLayer(0).setEnabled(False)
            else:
                city_line_layer.renderer().rootRule().children()[0].symbol().symbolLayer(0).setEnabled(False)
                city_line_layer.renderer().rootRule().children()[1].symbol().symbolLayer(0).setEnabled(False)

    # 设置县名、县界显隐
    for county_label_name in ['AGNP_X1']:
        if county_label_name in layer_names:
            county_label_layer = project.mapLayersByName(county_label_name)[0]
            for county_symbol_rule in county_label_layer.renderer().rootRule().children():
                county_symbol_rule.symbol().symbolLayer(0).setEnabled(county_show)
            for county_label_rule in county_label_layer.labeling().rootRule().children():
                county_label_rule.settings().drawLabels = county_show
    for county_line_name in ['BOUA_X']:
        if county_line_name in layer_names:
            county_line_layer = project.mapLayersByName(county_line_name)[0]
            for county_line_rule in county_line_layer.renderer().rootRule().children():
                county_line_rule.symbol().symbolLayer(0).setEnabled(county_show)

    # 设置河流名、线显隐
    for river_label_name in ['NAME_SEA']:
        if river_label_name in layer_names:
            river_label_layer = project.mapLayersByName(river_label_name)[0]
            for river_label_rule in river_label_layer.labeling().rootRule().children():
                river_label_rule.settings().drawLabels = r1_show
    for river_line_name in ['PHYDL_china', 'PHYDL_2']:
        if river_line_name in layer_names:
            river_line_layer = project.mapLayersByName(river_line_name)[0]
            for river_line_rule in river_line_layer.renderer().rootRule().children():
                river_line_rule.symbol().symbolLayer(0).setEnabled(r1_show)
    for river_label_name in ['NAME_L2']:
        if river_label_name in layer_names:
            river_label_layer = project.mapLayersByName(river_label_name)[0]
            for river_label_rule in river_label_layer.labeling().rootRule().children():
                river_label_rule.settings().drawLabels = r2_show
    for river_line_name in ['RIVER_L2']:
        if river_line_name in layer_names:
            river_line_layer = project.mapLayersByName(river_line_name)[0]
            for river_line_rule in river_line_layer.renderer().rootRule().children():
                river_line_rule.symbol().symbolLayer(0).setEnabled(r2_show)
    for river_label_name in ['NAME_L3']:
        if river_label_name in layer_names:
            river_label_layer = project.mapLayersByName(river_label_name)[0]
            for river_label_rule in river_label_layer.labeling().rootRule().children():
                river_label_rule.settings().drawLabels = r3_show
    for river_line_name in ['RIVER_L3']:
        if river_line_name in layer_names:
            river_line_layer = project.mapLayersByName(river_line_name)[0]
            for river_line_rule in river_line_layer.renderer().rootRule().children():
                river_line_rule.symbol().symbolLayer(0).setEnabled(r3_show)

    # 设置铁路显隐
    for railroad_line_name in ['RailRoads']:
        if railroad_line_name in layer_names:
            railroad_line_layer = project.mapLayersByName(railroad_line_name)[0]
            for railroad_symbol_rule in railroad_line_layer.renderer().rootRule().children():
                railroad_symbol_rule.symbol().symbolLayer(0).setEnabled(railroads_show)
                railroad_symbol_rule.symbol().symbolLayer(1).setEnabled(railroads_show)
            for railroad_symbol_rule in railroad_line_layer.labeling().rootRule().children():
                railroad_symbol_rule.settings().drawLabels = railroads_show

    # 设置国道显隐
    for guodao_line_name in ['roa_ln_GuoDao']:
        if guodao_line_name in layer_names:
            guodao_line_layer = project.mapLayersByName(guodao_line_name)[0]
            for guodao_symbol_rule in guodao_line_layer.renderer().rootRule().children():
                guodao_symbol_rule.symbol().symbolLayer(0).setEnabled(roads_guodao_show)
    for guodao_label_name in ['main_road_mark']:
        if guodao_label_name in layer_names:
            guodao_label_layer = project.mapLayersByName(guodao_label_name)[0]
            for guodao_label_rule in guodao_label_layer.labeling().rootRule().children():
                guodao_label_rule.settings().drawLabels = roads_guodao_show

    # 设置省道显隐
    for shengdao_line_name in ['roa_ln_ShengLu']:
        if shengdao_line_name in layer_names:
            shengdao_line_layer = project.mapLayersByName(shengdao_line_name)[0]
            for shengdao_line_rule in shengdao_line_layer.renderer().rootRule().children():
                shengdao_line_rule.symbol().symbolLayer(0).setEnabled(roads_shengdao_show)
    for shengdao_label_name in ['all_road_mark']:
        if shengdao_label_name in layer_names:
            shengdao_label_layer = project.mapLayersByName(shengdao_label_name)[0]
            for shengdao_label_rule in shengdao_label_layer.labeling().rootRule().children():
                shengdao_label_rule.settings().drawLabels = roads_shengdao_show


def merge_and_draw_legends(data_layers, project, layout, map_sizes, map_dpi, legend_layout_dpi, legend_font_dpi, ratio):
    leg_layers = [data_layer for data_layer in data_layers if 'legend' in data_layer]
    sorted(leg_layers, key=lambda x: x['legend']['merge'])
    merge_legs_layers = list()
    for leg_layer in leg_layers:
        if leg_layer['legend']['merge'] != 0:
            if len(merge_legs_layers) == 0:
                merge_legs_layers.append(leg_layer)
            else:
                if merge_legs_layers[-1]['legend']['merge'] == leg_layer['legend']['merge']:
                    merge_legs_layers.append(leg_layer)
                else:
                    # 多个合并图例情况
                    qgis_util_mm.add_legend_interact_edit(project, layout, merge_legs_layers, map_sizes,
                                                          map_dpi=map_dpi, layout_dpi=legend_layout_dpi,
                                                          font_dpi=legend_font_dpi, ratio=ratio)
                    merge_legs_layers.clear()
                    merge_legs_layers.append(leg_layer)
        else:
            qgis_util_mm.add_legend_interact_edit(project, layout, [leg_layer], map_sizes,
                                                  map_dpi=map_dpi, layout_dpi=legend_layout_dpi,
                                                  font_dpi=legend_font_dpi, ratio=ratio)
    if len(merge_legs_layers) > 0:
        qgis_util_mm.add_legend_interact_edit(project, layout, merge_legs_layers, map_sizes,
                                              map_dpi=map_dpi, layout_dpi=legend_layout_dpi,
                                              font_dpi=legend_font_dpi, ratio=ratio)


def make_pic(project_path, data_layers, png_path, crs, map_data, south_sea_map_show, south_sea_map, prov_para,
             city_para, county_para, beijing_para,  railroads_para, roads_guodao_para, roads_shengdao_para,
             river_para, station_para, text_para, symbol_para, server_type):
    """
    制图
    :param project_path: 工程文件的路径
    :param data_layers: 数据图层的参数
    :param png_path: 出图的路径
    :param crs: 工程的坐标系
    :param map_data: 底图的参数
    :param south_sea_map_show: 南海小地图的显示标识
    :param south_sea_map: 南海小地图组件的参数
    :param prov_para: 省标注的参数
    :param city_para: 市标注的参数
    :param county_para: 县标注的参数
    :param beijing_para: 北京标注的参数
    :param railroads_para: 铁路标注的参数
    :param roads_guodao_para: 公路国道标注的参数
    :param roads_shengdao_para: 公路省道标注的参数
    :param river_para: 河流标注的参数
    :param station_para: 国家、区域站点的参数
    :param text_para: 文字的参数
    :param symbol_para: logo的参数
    :param map_scale: 底图比例尺
    :return: None
    """

    # 环境
    qgs = QgsApplication([], False)  # 将第二个参数设置为False将禁用GUI
    qgs.initQgis()  # 加载提供程序
    project = QgsProject()  # 工程对象
    project.read(project_path)
    qgis_util_mm.add_crs(project, crs)  # 添加坐标系
    layout = QgsPrintLayout(project)  # 模板
    layout.initializeDefaults()
    layout.setBackgroundBrush(QColor(255, 255, 255))  # 背景颜色：白色
    map_dpi = map_data['dpi']
    layout.renderContext().setDpi(map_dpi)

    # 通过wms读取geoserver图层
    # wms_layers = ['BOUL_G', 'PBOULN', 'PHYDA', 'RIVER_L2', 'RIVER_L3', 'PHYDL_china', 'PHYDL_2', 'BOUA_S_tdh', 'PROULN_SJ',
    #               'BOUA_S', 'AGNP_SHCS', 'SD', 'NAME_SEA', 'NAME_L2', 'NAME_L3', 'BOUA_D', 'BOUA_X', 'AGNP_D11',
    #               'AGNP_X1', 'BOUL_JDX', 'NHDY', 'SEA_islands', 'CHINAOUT_MASK', 'SEA_MASK', 'Chinasea',
    #               'CHINAIN_MASK']
    # for wms_layer in wms_layers[::-1]:
    #     wms_url = 'url=http://10.10.31.23:8080/geoserver/wms?' \
    #               'request=GetMap&' \
    #               'service=WMS&' \
    #               'version=1.1.0&' \
    #               f'layers=STD-CHN-EDIT_WMS_{wms_layer}&' \
    #               'styles=&' \
    #               'crs=EPSG:45599&' \
    #               f'width={map_data["width"]}&' \
    #               f'height={map_data["height"]}&' \
    #               f'bbox={map_data["bbox"][0]},{map_data["bbox"][1]},{map_data["bbox"][2]},{map_data["bbox"][3]}&' \
    #               'format=image/png'
    #     base_map_layer = QgsRasterLayer(wms_url, wms_layer, 'wms')
    #     if not base_map_layer.isValid():
    #         print(base_map_layer.error().message())
    #     else:
    #         project.addMapLayer(base_map_layer)

    # 通过wms读取站点
    if station_para['showType'] == '1':
        station_wms_layer = 'STATION1'
    elif station_para['showType'] == '2':
        station_wms_layer = 'STATION2'
    elif station_para['showType'] == '3':
        station_wms_layer = 'STATION3'
    else:
        station_wms_layer = ''
    if station_wms_layer:
        wms_url = 'url=http://10.10.31.23:8080/geoserver/wms?' \
                  'request=GetMap&' \
                  'service=WMS&' \
                  'version=1.1.0&' \
                  f'layers=STD-CHN-EDIT_WMS_{station_wms_layer}&' \
                  'styles=&' \
                  'crs=EPSG:45599&' \
                  f'width={map_data["width"]}&' \
                  f'height={map_data["height"]}&' \
                  f'bbox={map_data["bbox"][0]},{map_data["bbox"][1]},{map_data["bbox"][2]},{map_data["bbox"][3]}&' \
                  'format=image/png'
        base_map_layer = QgsRasterLayer(wms_url, station_wms_layer, 'wms')
        if not base_map_layer.isValid():
            print(base_map_layer.error().message())
        else:
            project.addMapLayer(base_map_layer)

    # 添加数据图层
    qgis_util_mm.add_layer(data_layers, project, display_control=map_data['displayControl'], flag='interact_edit', layout_dpi=80)

    # 根据页面样式，改变字体等转换分辨率
    if server_type == 'rp0':
        text_font_dpi = 92
        legend_layout_dpi = 110
        legend_font_dpi = 80
        pccr_font_dpi = 90
        small_map_width = 28.83
        small_map_height = 39.48
        if round(float(map_data['width']) / float(map_data['height']), 1) == 1.2:
            map_width_chn = 233.8
            map_height_chn = 194.6
        elif round(float(map_data['width']) / float(map_data['height']), 1) == 1.3:
            map_width_chn = 233.8
            map_height_chn = 175.0
        else:
            map_width_chn = 233.8
            map_height_chn = 131.04
    elif server_type == 'rp1':
        text_font_dpi = 90
        legend_layout_dpi = 90
        legend_font_dpi = 90
        pccr_font_dpi = 120
        small_map_width = 34.72
        small_map_height = 47.55
        if round(float(map_data['width']) / float(map_data['height']), 1) == 1.2:
            map_width_chn = 323.12
            map_height_chn = 269.08
        elif round(float(map_data['width']) / float(map_data['height']), 1) == 1.3:
            map_width_chn = 323.12
            map_height_chn = 242.2
        else:
            map_width_chn = 323.12
            map_height_chn = 181.15
    elif server_type == 'rp2':
        text_font_dpi = 70
        legend_layout_dpi = 68
        legend_font_dpi = 90
        pccr_font_dpi = 100
        small_map_width = 46.41
        small_map_height = 63.56
        if round(float(map_data['width']) / float(map_data['height']), 1) == 1.2:
            map_width_chn = 394.52
            map_height_chn = 328.44
        elif round(float(map_data['width']) / float(map_data['height']), 1) == 1.3:
            map_width_chn = 394.52
            map_height_chn = 295.68
        else:
            map_width_chn = 394.52
            map_height_chn = 221.19
    else:
        text_font_dpi = 92
        legend_layout_dpi = 90
        legend_font_dpi = 90
        pccr_font_dpi = 72
        small_map_width = 34.72
        small_map_height = 47.55
        if round(float(map_data['width']) / float(map_data['height']), 1) == 1.2:
            map_width_chn = 287.28
            map_height_chn = 239.12
        elif round(float(map_data['width']) / float(map_data['height']), 1) == 1.3:
            map_width_chn = 287.28
            map_height_chn = 215.04
        else:
            map_width_chn = 287.28
            map_height_chn = 161.0

    # 底图
    # map_width = float(mapData['width']) / mapData['dpi'] * 25.4
    # map_height = float(mapData['height']) / mapData['dpi'] * 25.4
    # map_width = float(map_data['width'])
    # map_height = float(map_data['height'])
    # map_width = 273.84
    # map_height = 228.07
    # map_width_chn = (map_data['bbox'][2] - map_data['bbox'][0]) / float(map_data['mapScale']) * 1000
    # map_height_chn = (map_data['bbox'][3] - map_data['bbox'][1]) / float(map_data['mapScale']) * 1000
    # print('>'*20, '图片宽高：', map_width_chn, map_height_chn)
    if any([x for x in ['etno', 'wtno', 'hano', 'hghr', 'jhui', 'jhan', 'jnan', 'haso', 'wtso', 'jjjq', 'haet', 'hawt']
            if x in map_data['baseMapName']]):
        map_width = 283.3
        map_height = 236
    elif any([x for x in ['chaj'] if x in map_data['baseMapName']]):
        map_width = 600
        map_height = 300
    elif any([x for x in
              ['chju', 'hnhu', 'huhd', 'nmg', 'jil', 'hlj', 'jgs', 'snd', 'gnd', 'gnx', 'han', 'giz', 'xiz', 'gns', 'qgh',
               'xnj'] if x in map_data['baseMapName']]):
        map_width = 400
        map_height = 300
    elif any([x for x in
              ['chjm', 'hnhd', 'huhu', 'liao', 'sohj', 'sonl', 'taih', 'zhj', 'zhjb', 'zhjs', 'bej', 'lin', 'zhj',
               'hen', 'hun', 'chq', 'sic', 'ynn'] if x in map_data['baseMapName']]):
        map_width = 400
        map_height = 400
    elif any([x for x in ['chjd', 'huhm'] if x in map_data['baseMapName']]):
        map_width = 450
        map_height = 337.5
    elif any([x for x in ['hnhe'] if x in map_data['baseMapName']]):
        map_width = 600
        map_height = 337.5
    elif any([x for x in ['hnhm', 'zhjd'] if x in map_data['baseMapName']]):
        map_width = 300
        map_height = 400
    elif any([x for x in ['huhe'] if x in map_data['baseMapName']]):
        map_width = 500
        map_height = 375
    elif any([x for x in ['haih'] if x in map_data['baseMapName']]):
        map_width = 350
        map_height = 437.5
    elif any([x for x in ['zhjx'] if x in map_data['baseMapName']]):
        map_width = 640
        map_height = 358
    elif any([x for x in ['taj', 'snx', 'jgx', 'shx', 'ngx', 'taw'] if x in map_data['baseMapName']]):
        map_width = 300
        map_height = 450
    elif any([x for x in ['heb', 'shh', 'anh', 'fuj'] if x in map_data['baseMapName']]):
        map_width = 400
        map_height = 500
    elif any([x for x in ['hub'] if x in map_data['baseMapName']]):
        map_width = 480
        map_height = 270
    else:
        map_width = map_width_chn
        map_height = map_height_chn
    ratio = ((map_width_chn / map_width) + (map_height_chn / map_height)) / 2
    print('>' * 20, 'ratio', ratio)
    map_sizes = {
        'map_width': float(map_width),
        'map_height': float(map_height),
        'map_width_org': float(map_data['width']),
        'map_height_org': float(map_data['height']),
    }
    # print('>'*20, map_width, map_height)
    map_data['bbox'] = qgis_util_mm.transform_bounding(project, crs, map_data['bbox'])  # 转换边界
    big_map = {
        'referencepoint': 0,
        'positiononpagewidth': 0,
        'positiononpageheight': 0,
        'width': map_width,
        'height': map_height,
        'xmin': map_data['bbox'][0],
        'xmax': map_data['bbox'][2],
        'ymin': map_data['bbox'][1],
        'ymax': map_data['bbox'][3],
        'framestrokewidth': 0.5
    }
    qgis_util_mm.add_map(layout, big_map)

    # 文字
    if text_para:
        for text_para in text_para:
            if text_para and 'content' in text_para and text_para['content']:
                qgis_util_mm.add_text_customized(layout, text_para, map_sizes, map_dpi=map_dpi)

    # 图标
    if symbol_para:
        # symbol_para.update({
        #     'path': settings.logo_path
        # })
        qgis_util_mm.add_svg(layout, symbol_para, map_sizes)

    # 图例
    # 如果有并列图例，将相邻图例的边框线去掉
    initial_frames = []
    app_legs_layers = [data_layer for data_layer in data_layers if 'legend' in data_layer and data_layer['legend']['referencepoint'] == 0]
    for data_layer in app_legs_layers[::-1]:
        pass
    # 如果有合并图例参数，将所有数据图例合并到一个图例中
    merge_legs_layers = copy.deepcopy(data_layers)
    merge_legend_para = dict()
    for data_layer in merge_legs_layers:
        if data_layer['dataType'] == 'merge':
            merge_legend_para = data_layer['legend']
            data_layers.remove(data_layer)
            merge_legs_layers.remove(data_layer)
    if merge_legend_para:
        for data_layer in merge_legs_layers:
            if 'Mark' not in data_layer['dataType']:
                data_layer['legend'] = merge_legend_para
                data_layer['legend']['merge'] = 999
        merge_legs_layers = merge_legs_layers[::-1]
        merge_and_draw_legends(merge_legs_layers, project, layout, map_sizes, map_dpi, legend_layout_dpi, legend_font_dpi, ratio)
    # 按原参数，添加图例
    merge_and_draw_legends(data_layers, project, layout, map_sizes, map_dpi, legend_layout_dpi, legend_font_dpi, ratio)

    # 注记
    # qgis_util.add_annotation(project, 1392.96, 3380874.51)
    # project.annotationManager()
    # QgsAnnotationManager()
    # qgis_util.add_annotation(project, 1600.96, 4000874.51)

    # 修改省市县河流标注
    if any([x for x in ['chnScale', 'Processchn'] if x in map_data['baseMapName']]):
        modify_labeling(project, prov_para, 'prov', server_type, font_dpi=pccr_font_dpi)
        modify_labeling(project, city_para, 'city', server_type, font_dpi=pccr_font_dpi)
        modify_labeling(project, county_para, 'county', server_type, font_dpi=pccr_font_dpi)
        modify_labeling(project, beijing_para, 'beijing', server_type, font_dpi=pccr_font_dpi)
        modify_labeling(project, railroads_para, 'railroads', server_type, font_dpi=pccr_font_dpi)
        modify_labeling(project, roads_guodao_para, 'roads_guodao', server_type, font_dpi=pccr_font_dpi)
        modify_labeling(project, roads_shengdao_para, 'roads_shengdao', server_type, font_dpi=pccr_font_dpi)
        modify_labeling_river(project, river_para, font_dpi=pccr_font_dpi)
        show_city_county_river_labels_lines(project, city_para, county_para, river_para, railroads_para,
                                            roads_guodao_para, roads_shengdao_para)

    base_map_name = os.path.basename(project_path)
    # 南海小地图
    if south_sea_map_show:
        # small_map_width = float(southSeaMap['width']) / mapData['dpi'] * 25.4
        # small_map_height = float(southSeaMap['height']) / mapData['dpi'] * 25.4
        # small_map_width = 30.66
        # small_map_height = 42
        # small_map_width = float(south_sea_map['width'])
        # small_map_height = float(south_sea_map['height'])
        if 'STDhanScaleNh' in base_map_name:  # 需要海南省mm底图???
            # 海南底图，加小地图时参数有变
            small_map_bbox = [300000, 50000, 1900000, 2500000]
            small_map_width = (small_map_bbox[2] - small_map_bbox[0]) / 43763780 * 1000
            small_map_height = (small_map_bbox[3] - small_map_bbox[1]) / 43763780 * 1000
            small_map_bbox = qgis_util_mm.transform_bounding(project, crs, small_map_bbox)
            small_map_para = {
                'referencepoint': 0,
                'positiononpagewidth': 0,
                'positiononpageheight': 0,
                'width': small_map_width,
                'height': small_map_height,
                'xmin': small_map_bbox[0],
                'xmax': small_map_bbox[2],
                'ymin': small_map_bbox[1],
                'ymax': small_map_bbox[3],
                'framestrokewidth': 0.25
            }
            small_map_name_para = {
                'referencepoint': 8,
                'positiononpagewidth': small_map_width,
                'positiononpageheight': small_map_height - 4,
                'font': '宋体',
                'fontsize': 5,
                'bold': 'false',
                'backgroundcolor': 'false',
                'halign': 1,
                'width': 20,
                'height': 7
            }
            small_map_scale_para = {
                'referencepoint': 8,
                'positiononpagewidth': small_map_width,
                'positiononpageheight': small_map_height - 2,
                'font': '宋体',
                'fontsize': 5,
                'bold': 'false',
                'backgroundcolor': 'false',
                'halign': 1,
                'width': 20,
                'height': 7
            }
            small_map_layout = layout.clone()
            for item in small_map_layout.items():
                if isinstance(item, QgsLayoutItemMap):
                    small_map_layout.removeLayoutItem(item)
            qgis_util_mm.add_map(small_map_layout, small_map_para)
            small_map_name_text = settings.small_map_name
            qgis_util_mm.add_text_adjust(small_map_layout, small_map_name_para, small_map_name_text, font_dpi=68)
            small_map_scale_text = settings.small_map_scale
            qgis_util_mm.add_text_adjust(small_map_layout, small_map_scale_para, small_map_scale_text, font_dpi=68)
            small_map_pic_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'temp', 'han_nh.png')
            if os.path.exists(small_map_pic_path):
                os.remove(small_map_pic_path)
            qgis_util_mm.layout_exporter(small_map_layout, small_map_pic_path)  # 小地图单独出图
            project.layerTreeRoot().findGroup('group1').removeAllChildren()  # 出完小地图之后需要删除多余图层
            small_map_pic_para = {
                'path': small_map_pic_path,
                'referencepoint': 8,
                'positiononpagewidth': map_width - 1.5,
                'positiononpageheight': map_height - 3,
                'width': small_map_width,
                'height': small_map_height
            }
            qgis_util_mm.add_svg(layout, small_map_pic_para, layout_dpi=25.4)  # 将小地图贴到大图中
            if os.path.exists(small_map_pic_path):
                os.remove(small_map_pic_path)
        else:
            small_map_bbox = [335000, 255000, 1905000, 2405000]
            # small_map_width = (small_map_bbox[2] - small_map_bbox[0]) / float(south_sea_map['mapScale']) * 1000
            # small_map_height = (small_map_bbox[3] - small_map_bbox[1]) / float(south_sea_map['mapScale']) * 1000
            small_map_width = float(south_sea_map['width']) / float(map_data['width']) * map_width
            small_map_height = float(south_sea_map['height']) / float(map_data['height']) * map_height
            # print('>'*20, '南海宽高：', small_map_width, small_map_height)
            small_map_bbox = qgis_util_mm.transform_bounding(project, crs, small_map_bbox)
            small_map_para = {
                'referencepoint': 6,
                'positiononpagewidth': 1.5,
                'positiononpageheight': map_height - 3,
                'width': small_map_width,  # map_width * 0.12,
                'height': small_map_height,  # map_height * 0.18,
                'xmin': small_map_bbox[0],
                'xmax': small_map_bbox[2],
                'ymin': small_map_bbox[1],
                'ymax': small_map_bbox[3],
                'framestrokewidth': 0.25
            }
            small_map_name_para = {
                'referencepoint': 6,
                'positiononpagewidth': small_map_width - 10,
                'positiononpageheight': map_height - 6,
                'font': '宋体',
                'fontsize': 3,
                'bold': 'false',
                'backgroundcolor': 'false',
                'halign': 1,
                'width': 10,
                'height': 4
            }
            small_map_scale_para = {
                'referencepoint': 6,
                'positiononpagewidth': small_map_width - 15,
                'positiononpageheight': map_height - 3,
                'font': '宋体',
                'fontsize': 3,
                'bold': 'false',
                'backgroundcolor': 'false',
                'halign': 1,
                'width': 15,
                'height': 4
            }
            qgis_util_mm.add_map(layout, small_map_para)
            small_map_name_text = settings.small_map_name
            qgis_util_mm.add_text_adjust(layout, small_map_name_para, small_map_name_text)
            small_map_scale_text = settings.small_map_scale
            qgis_util_mm.add_text_adjust(layout, small_map_scale_para, small_map_scale_text)

    # 打印所有图层
    print(f'>>> layers <<<:')
    for i in project.layerTreeRoot().layerOrder():
        print(i)

    # 出图
    print(f'>>> png_path <<<:\n{png_path}')
    qgis_util_mm.layout_exporter(layout, png_path, image_size=[map_width, map_height])
    qgs.quit()


if __name__ == '__main__':

    cbfile = './data/colorbar_CLM.txt'

    cblist, cbtitle = GetColorList(cbfile)
    print(cblist)

    colorbar('./data/clm.png', cblist,  cbtitle=cbtitle)
