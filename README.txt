-*- encoding:UTF-8 -*-
function name: txt2pic
author: zzq889@gmail.com
usage: 利用PIL模块把文字转化成图片
api使用说明：

text = '中文字符'
text.decode('utf-8')
txt2pic(msg = text,
	font = [ 字体路径1, 字体路径2, ... ], 默认simhei
	fontsize = 字体大小, 默认32
	fgcolor = (r, g, b), 默认(0,0,0)
	bgcolor = (r, g, b, alpha), 默认(255,255,255,255)
	background = 背景图片路径, 默认None
	padding = 字的间距,（int类型或者tuple类型，如果是tuple取前四个值，
			包括 上、右、下、左 四个间距的值）默认4
	filters = { 滤镜1:滤镜执行次数, 滤镜2:滤镜执行次数, ... }, 默认None
		滤镜包括：BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, 
			EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, 
			SMOOTH, SMOOTH_MORE, SHARPEN, NOISE
			其中NOISE用法特例：'NOISE':(39,35)
			表示在噪音出现的概率为(39-35)/39
	trans = [ 变换1, 变换2, ... ],  默认None
		转换包括：
		FLIP_LEFT_RIGHT, 水平翻转
		FLIP_TOP_BOTTOM, 垂直翻转
		ROTATE_[?]_[METHOD] 旋转方法
        	#METHOD:
        	NEAREST 最近
        	BILINEAR 双线型
        	BICUBIC 双三次插值
        	ANTIALIAS 平滑
		例如：'rotate_30_bilinear' 表示以二次线性逆时针旋转30度
	re_size = (width, height), 放大缩小图像
	filename = 文件名（后缀名）, 根据后缀名自动判断类型，默认PNG
	)
