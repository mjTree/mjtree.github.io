# coding:utf-8
# time: 2024/4/11 6:58 下午
import os
import math
from PIL import Image


class VectorCompare:
    # 计算矢量大小
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    # 计算矢量之间cos值
    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.items():
            if concordance2.get(word):
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


# 将图片转换为矢量
def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1


v = VectorCompare()
iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
           'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

work_path = os.path.dirname(__file__)
# 加载训练集
imageset = []
for letter in iconset:
    for img in os.listdir(os.path.join(work_path, 'iconset/%s/' % (letter))):
        temp = []
        if img != 'Thumbs.db' and img != '.DS_Store':
            temp.append(buildvector(Image.open(os.path.join(work_path, 'iconset/%s/%s') % (letter, img))))
        imageset.append({letter: temp})

im = Image.open('0q1d10.gif')
im.convert('P')  # 将图片转换为8位像素模式
im2 = Image.new('P', im.size, 255)
temp = {}

# 构造黑白二值图片
for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y, x))
        temp[pix] = pix
        # 220和227是需要的红色和灰色
        if pix == 220 or pix == 227:
            im2.putpixel((y, x), 0)
im2.show()

# 获取每个字符开始和结束的列序号
inletter = False
foundletter = False
start = end = 0
letters = []

for y in range(im2.size[0]):
    for x in range(im2.size[1]):
        pix = im2.getpixel((y, x))
        if pix != 255:
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = y
    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start, end))
    inletter = False

# 对验证码图片进行切割
for letter in letters:
    im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
    guess = []
    # 将切割得到的验证码小片段与每个训练片进行比较
    for image in imageset:
        for x, y in image.items():
            if len(y) != 0:
                guess.append((v.relation(y[0], buildvector(im3)), x))

    guess.sort(reverse=True)
    print(guess[0])
