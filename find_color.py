from PIL import Image  # pip install Pillow

img = Image.open('tank.png')
q, w = img.size
qwe_2 = []
for i in range(35):
    qwe = []
    for i_2 in range(40):
        qwe.append(img.getpixel((i_2 - 1, i - 1))[:3])
    qwe_2.append(qwe)

if __name__ == '__main__':
    print(len(qwe_2))
