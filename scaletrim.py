#!/usr/bin/env python2.2

from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageChops

import sys, os

aspect = lambda (h,v): float(h) / float(v)

if len(sys.argv) < 3:
    print "usage: scaletrim WxH file ..."
    sys.exit(1)

target_size = [int(x) for x in sys.argv[1].split('x')]
target_aspect = aspect(target_size)

def center_rect(outer, inner):
    (inw, inh) = (inner[2] - inner[0], inner[3] - inner[1])
    (outw, outh) = (outer[2] - outer[0], outer[3] - outer[1])
    topleft = (outer[0] + (outw - inw)/2, outer[1] + (outh - inh)/2)
    return (
        topleft[0], topleft[1],
        topleft[0] + inw, topleft[1] + inh
    )

def debug_show_images(imagelist):
    from Tkinter import Tk, Canvas, LEFT, BOTH, NW
    from PIL import ImageTk
    root = Tk()
    items = []
    for im in imagelist:
        canvas = Canvas(root, height=im.size[1], width=im.size[0])
        canvas.pack(side='left')
        photo = ImageTk.PhotoImage(im)
        items.append(photo)
        item = canvas.create_image(0,0,anchor='nw',image=photo)
    mainloop()

GAUSSIAN_BLUR_5X5 = ImageFilter.Kernel((5,5),
    (0,1,2,1,0,
     1,2,4,2,1,
     2,4,8,2,2,
     1,2,4,2,1,
     0,1,2,1,0))

GAUSSIAN_BLUR_5X5_2 = ImageFilter.Kernel((5,5),
     (0,1,2,1,0,
      1,2,3,2,1,
      2,3,4,3,2,
      1,2,3,2,1,
      0,1,2,1,0))

GAUSSIAN_BLUR_5X5_3 = ImageFilter.Kernel((5,5),
   (0.5,  2,  3,  2,0.5,
      2,  3,3.5,  3,  2,
      3,3.5,  4,3.5,  3,
      2,  3,3.5,  3,  2,
    0.5,  2,  3,  2,0.5,))

def make_interior_shadow(im, (left,top,right,bottom), shadowcolor):
    pad = 10 # so the kernel can work across every pixel
    shadow = Image.new('RGB', (im.size[0] + 2*pad, im.size[1] + 2*pad), color='#ffffff')
    d = ImageDraw.Draw(shadow)
    if top > 0:
        d.rectangle((0, 0, shadow.size[0], pad+top), fill=shadowcolor)
    if left > 0:
        d.rectangle((0, 0, pad+left, shadow.size[1]), fill=shadowcolor)
    if right > 0:
        d.rectangle((0, shadow.size[1]-pad-right, shadow.size[0], shadow.size[1]), fill=shadowcolor)
    if bottom > 0:
        d.rectangle((shadow.size[0]-pad-bottom, 0, shadow.size[0], shadow.size[1]), fill=shadowcolor)
    del d
    shadow = shadow.filter(GAUSSIAN_BLUR_5X5_3).filter(GAUSSIAN_BLUR_5X5_3)
    shadow = shadow.crop((pad,pad,im.size[0]+pad,im.size[1]+pad))
    return shadow

def add_interior_shadow(im, darkness=1.0, top=4, left=4, right=0, bottom=0):
    if im.mode != 'RGB':
        im = im.convert('RGB')
    return ImageChops.multiply(im, make_interior_shadow(im, 
        (left, top, right, bottom),
        shadowcolor='#%(x)02x%(x)02x%(x)02x' % dict(x=((1.0-darkness)*255))))

def main():
    import random
    
    BLOWUP = 1.5
    RANDOM_PAN = True
    
    for fn in sys.argv[2:]:
        fname, ext = os.path.splitext(fn)
    
        sys.stderr.write("(")
    
        im = Image.open(fn)
        im_aspect = aspect(im.size)
    
        sys.stderr.write("[image %s %dx%d aspect %.2f]" % (fn, im.size[0], im.size[1], im_aspect))
    
        if target_aspect > im_aspect: # target is "wider" than image
            scale = float(target_size[0]) / float(im.size[0])
        else: # target is "taller"
            scale = float(target_size[1]) / float(im.size[1])
            
        scale *= BLOWUP
    
        sys.stderr.write("[scale %d%%]" % (scale*100))
        im = im.resize(
            [int(scale*x) for x in im.size],
            Image.ANTIALIAS)
    
        if RANDOM_PAN:
            cropcoord = (random.randrange(0, im.size[0]-target_size[0]),
                        random.randrange(0, im.size[1]-target_size[1]))
            croprect = (cropcoord[0], cropcoord[1], 
                cropcoord[0] + target_size[0], cropcoord[1] + target_size[1])
        else:
            croprect = center_rect((0,0,im.size[0],im.size[1]), 
                                   (0,0,target_size[0],target_size[1]))
        sys.stderr.write("[crop to (%s)]" % (','.join(str(x) for x in croprect)))
        im = im.crop(croprect)
    
        # im = im.filter(ImageFilter.Kernel((3,3), 
        #                 (-.5, -.5, -.5,
        #                  -.5,   5, -.5, 
        #                  -.5, -.5, -.5)))
        im = im.filter(ImageFilter.DETAIL)
    
    #     d = ImageDraw.Draw(im)
    #     d.rectangle((0,0,im.size[0]-1, im.size[1]-1), outline="#000000")
    #     del d

        im = add_interior_shadow(im, top=3, left=3, right=1, bottom=1, darkness=0.5)
    
        im.save(fname + '.trim' + ext)

        sys.stderr.write("[save %dx%d to %s]" % (im.size[0], im.size[1], fname + '.trim' + ext))
        sys.stderr.write(")\n")
        
if __name__ == '__main__': main()