from PIL import Image


def alienImageManip(image,image_name,red,green,blue):
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    img = Image.open(image)
    # img = Image.new( 'RGB', (250,250), "black") # create a new black image
    pixels = img.load() # create the pixel map

    for i in range(img.size[0]):    # for every col:
        for j in range(img.size[1]):    # For every row
            p = pixels[i,j]
            # print(str(i) + ',' + str(j) + ',' + str(p))
            if p[0] == 0 and p[1] == 0 and p[2] == 0 and p[3] > 50:
                pixels[i,j] = (red,green,blue) #(i, j, 100) # set the colour accordingly
    img.save(image_name)
    # img.show(image_name)


alienImageManip('images/alien_hands_up.png','images/alien_hands_up_green.png',102,204,0)
alienImageManip('images/alien_hands_down.png','images/alien_hands_down_yellow.png',255,255,0)
alienImageManip('images/king_invader.png','images/king_invader_red.png',255,0,0)
