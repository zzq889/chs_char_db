#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 
import Image,ImageDraw,ImageFont
import os
import hashlib

#def txt2pic(msg,fontsize=12,spacing=0,font='fonts/Arial.ttf',filetype='PNG',filename,imgfilter=None,background=None,bgcolor=None,fgcolor=None,padding=3):
def txt2png(msg,font='fonts/Arial.ttf',fontsize=12,background=None,bgcolor=None,fgcolor=None,padding=3):
	"""
	"函数将msg字符串生成一张图片
	"fontsize是字体大小，默认32×32
	"font是字体，随机显示每个文字的字体
	"filetype文件格式，默认PNG
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
	"padding是图片文字的内补丁，
	"    类似于CSS的padding，可以接受int类型和tuple类型，
	"    tuple类型取前4位
	"""
	#处理函数参数
	msg = msg if isinstance(msg,str) else str(msg)
	fontsize = fontsize if isinstance(fontsize,int) else 12
	try:
		font = ImageFont.truetype(font,fontsize)
	except IOError,e:
		return '%s' % e
	try:
		bg = Image.open(background)
	except (AttributeError,IOError):
		bg = None
	if isinstance(bgcolor,tuple) and len(bgcolor) == 3 and (0,0,0) <= bgcolor <= (255,255,255):
		pass
	else:
		bgcolor = (255,255,255)
	if isinstance(fgcolor,tuple) and len(fgcolor) == 3 and (0,0,0) <= fgcolor <= (255,255,255):
		pass
	else:
		fgcolor = (0,0,0)
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
	w,h = font.getsize(msg)
	w = w + right + left
	h = h + top + bottom
	im = Image.new('RGB',(w,h),bgcolor)
	if bg:
		im.paste(bg.crop((0,0,w,h)))
	d = ImageDraw.Draw(im)
	d.text((left,top),msg,font=font,fill=fgcolor)
	del d
	filename = '%s.png' % hashlib.md5(msg).hexdigest()
	try:
		im.save(filename,"PNG")
	except IOError,e:
		return '%s' % e
	else:
		return filename

txt2png('test')
