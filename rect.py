import Image, ImageDraw

def rectangle(input, box, fill, outline, width):
	d = ImageDraw.Draw(input)
	d.rectangle(box,fill=outline)
	d.rectangle(
		(box[0]+width,box[1]+width,box[2]-width,box[3]-width),
		fill=fill
	)

input = Image.new('RGBA',(40,40),(0,0,0,0))
rectangle(input,(0,0,39,39),"lightblue","blue",5)
input.save('rect.png',"PNG")
