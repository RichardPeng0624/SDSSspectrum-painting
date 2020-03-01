import os
from PIL import Image

width_i=720
height_i=360
row_max=1
line_max=61
all_path=[]
a=10
num=0
while a<11:
    for filename in os.listdir('/media/richard/Backup Plus/candidate_dr16_0.8')[400*a:400*(a+1)]:
        if filename.endswith('eps'):
            all_path.append(os.path.join('/media/richard/Backup Plus/candidate_dr16_0.8/',filename))
    toImage=Image.new('RGBA',(width_i*row_max,height_i*line_max))
    pic_max=line_max*row_max
    for i in range(0,row_max):
        for j in range(0,line_max):                
            pic_head=Image.open(all_path[num])
            width,height=pic_head.size
            tmppic=pic_head.resize((width_i,height_i))
            loc=(i*width_i,j*height_i,)
            toImage.paste(tmppic,loc)
            num=num+1
            if num+400*a>4060:
                continue
        continue
    toImage.save('/media/richard/Backup Plus/candidate_dr16_0.8/connection/%s.png'%a)
    print(a)
    all_path.clear()
    a+=1
    num=0
