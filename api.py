#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 
import Image,ImageDraw,ImageFont,ImageFilter,ImageEnhance
import os
from string import upper
import hashlib
import random
import time
from math import sqrt

def txt2pic(msg,
            font=['c:\Windows\Fonts\simhei.ttf'],
            fontsize=32,
            background=None,
            bgcolor=None,
            fgcolor=None,
            padding=4,
            filters={},
            trans=[],
            re_size=None,
            filename=None):
	"""
	"函数将msg字符串生成一张图片
	"fontsize是字体大小，默认32×32
	"font是字体，随机显示每个文字的字体
	"filetype文件格式，默认PNG，可自动根据文件后缀名判断类型
	"imgfilter变换（可以是多个，如果多个就都做）
         	加背景
         	加噪声
         	文字旋转
         	文字拉伸/缩小
         	加模糊
         	效果（各种滤镜）
	"background为背景图片，默认没有
	"bgcolor是背景颜色，默认为白色
	"fgcolor是文字颜色，默认为黑色
	"padding是图片文字的top,right,bottom,left间距，
	"    可以接受int类型和tuple类型，
	"    tuple类型取前4位
	"""
	#处理函数参数
	"msg = msg if isinstance(msg,str) else str(msg)"
        """font_path
	Linux: /usr/share/fonts/
        Max OS: /Library/Fonts/
        Windows: C:\Windows\Fonts\
        """
	fontsize = fontsize if isinstance(fontsize,int) else 32
	try:
		font = [ImageFont.truetype(x,fontsize) for x in font]
	except IOError,e:
		return '%s' % e
	try:
		bg = Image.open(background)
	except (AttributeError,IOError):
		bg = None
	if isinstance(bgcolor,tuple) and len(bgcolor) == 4 and (0,0,0,0) <= bgcolor <= (255,255,255,255):
		pass
	else:
		bgcolor = (255,255,255,255)
	if isinstance(fgcolor,tuple) and len(fgcolor) == 3 and (0,0,0) <= fgcolor <= (255,255,255):
		pass
	else:
		fgcolor = (0,0,0)
        #文字间距
	if isinstance(padding,tuple):
		pl = len(padding)
		padding = [x if isinstance(x,int) and x >= 0 else 3 for x in padding] * 4
		padding = padding[:4]
		top,right,bottom,left = padding
		if pl == 3:
			left = right
	elif isinstance(padding,int):
		top = right = bottom = left = padding
	else:
		top = right = bottom = left = 3
	w,h = font[0].getsize(msg[0])
	w = w + right + left
	h = h + top + bottom
	num_p_l = int(sqrt(len(msg)-1))+1
	im = Image.new('RGBA',(h*num_p_l,h*num_p_l),bgcolor)
	if bg:
		im.paste(bg.crop((0,0,h*num_p_l,h*num_p_l)))
        #print text
	d = ImageDraw.Draw(im)
	cur_left = left + (h-w)/2
	cur_top = top
	for i in range(len(msg)):
                d.text((cur_left,cur_top),msg[i],font=font[random.randint(0,len(font)-1 )],fill=fgcolor)
                if i % num_p_l == num_p_l - 1:
                        cur_top += h
                        cur_left = left + (h-w)/2
                else: cur_left += h
        del cur_left
        del cur_top
        del d
        
        #filters
        if isinstance(filters,dict):
        #BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN, NOISE
                for x in filters.keys():
                        if upper(x) == 'BLUR':
                                for i in range(filters[x]): im = im.filter( ImageFilter.BLUR )
                        elif upper(x) == 'CONTOUR':
                                for i in range(filters[x]): im = im.filter( ImageFilter.CONTOUR )
                        elif upper(x) == 'DETAIL':
                                for i in range(filters[x]): im = im.filter( ImageFilter.DETAIL )
                        elif upper(x) == 'EDGE_ENHANCE':
                                for i in range(filters[x]): im = im.filter( ImageFilter.EDGE_ENHANCE )
                        elif upper(x) == 'EDGE_ENHANCE_MORE':
                                for i in range(filters[x]): im = im.filter( ImageFilter.EDGE_ENHANCE_MORE )
                        elif upper(x) == 'EMBOSS':
                                for i in range(filters[x]): im = im.filter( ImageFilter.EMBOSS )
                        elif upper(x) == 'FIND_EDGES':
                                for i in range(filters[x]): im = im.filter( ImageFilter.FIND_EDGES )
                        elif upper(x) == 'SMOOTH':
                                for i in range(filters[x]): im = im.filter( ImageFilter.SMOOTH )
                        elif upper(x) == 'SMOOTH_MORE':
                                for i in range(filters[x]): im = im.filter( ImageFilter.SMOOTH_MORE )
                        elif upper(x) == 'SHARPEN':
                                for i in range(filters[x]): im = im.filter( ImageFilter.SHARPEN )
                        elif upper(x) == 'NOISE':
                                #散点噪音
                                d = ImageDraw.Draw(im)
                                for i in range(im.size[0]):
                                        for j in range(im.size[1]):
                                                flag = random.randint(0,filters[x][0])
                                                if flag > filters[x][1]:
                                                        d.point((i,j),fill = fgcolor)
                                del flag
                                del d
        #transpose
        if isinstance(trans,list):
        #FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM, ROTATE_[?]_[METHOD]
        #METHOD:
        #NEAREST 最近
        #BILINEAR 双线型
        #BICUBIC 双三次插值
        #ANTIALIAS 平滑
                for x in trans:
                        if upper(x) == 'FLIP_LEFT_RIGHT':
                                im = im.transpose( Image.FLIP_LEFT_RIGHT )
                        elif upper(x) == 'FLIP_TOP_BOTTOM':
                                im = im.transpose( Image.FLIP_TOP_BOTTOM )
                        elif upper(x) == 'STRECH':
                                #图形扭曲
                                para = [1-float(random.randint(1,2))/100,
                                0,
                                0,
                                0,
                                1-float(random.randint(1,10))/100,
                                float(random.randint(1,2))/500,
                                0.001,
                                float(random.randint(1,2))/500
                                ]
                                #print randStr,para
                                im = im.transform(im.size, Image.PERSPECTIVE,para)
                        #旋转
                        elif upper(x).split('_')[0] == 'ROTATE':
                                if upper(x).split('_')[-1] == 'NEAREST':
                                        im = im.rotate(int(upper(x).split('_')[1]),Image.BILINEAR,expand=True)
                                elif upper(x).split('_')[-1] == 'BILINEAR':
                                        im = im.rotate(int(upper(x).split('_')[1]),Image.BILINEAR,expand=True)
                                elif upper(x).split('_')[-1] == 'BICUBIC':
                                        im = im.rotate(int(upper(x).split('_')[1]),Image.BILINEAR,expand=True)
                                elif upper(x).split('_')[-1] == 'ANTIALIAS':
                                        im = im.rotate(int(upper(x).split('_')[1]),Image.BILINEAR,expand=True)
                                elif upper(x).split('_')[-1] == 'NONE':
                                        im = im.rotate(int(upper(x).split('_')[1]),expand=True)
                                else:
                                        im = im.rotate(int(upper(x).split('_')[1]),Image.BILINEAR,expand=True)
                                #fix picture size as square
                                if im.size[0] <> im.size[1]:
                                        im = im.crop((0,0,im.size[1],im.size[1]))

        #im = ImageEnhance.Contrast(im).enhance(3.0)
        if isinstance(re_size,tuple):
                im = im.resize( re_size,Image.BILINEAR )

        #save file
        if not isinstance(filename,str):
                filename = '%s.png' % time.time()
                #filename = '%s.png' % hashlib.md5(msg).hexdigest()
        filesplit = filename.split('.')[-1]
        filetype = 'jpeg' if filesplit == 'jpg' else filesplit
	try:
		im.save(filename,filetype,quality=100)
	except IOError,e:
		return '%s' % e
	else:
		return filename

if __name__ == '__main__':
        val = [unichr(random.randint(0x4E00, 0x9FBB)) for i in range(24)]
        #val = '文字输入测试文字输入测试'
        #val = [ x for x in val.decode('utf-8') ]
        txt2pic(
                msg=val,
                font=['c:\Windows\Fonts\simhei.ttf',
                      'c:\Windows\Fonts\simkai.ttf',
                      'c:\Windows\Fonts\simfang.ttf'],
                fontsize=32,
                fgcolor=(0,100,100),
                bgcolor=(100,200,200,255),
                background=None,
                padding=4,
                filters={'DETAIL':2,'NOISE':(39,35)},
                trans=['rotate_90_bilinear','flip_top_bottom'],
                re_size=(225,225),
                filename='test.png',
                )
