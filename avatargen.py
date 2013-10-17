import urllib2 as urllib
from cStringIO import StringIO
import Image

dim = 1

def width(img):
    """Gets the width of an image. Defined as its own thing for easiness."""
    return img.size[0]


def height(img):
    """Gets the height of an image. Defined as its own thing for easiness."""
    return img.size[1]


def size(img):
    """Gets the size of an image. Yes, I'm aware img.size is a thing, this is just so the above doesn't throw you off."""
    return (width(img),height(img))


def convert(img,threshold=128):
    """Converts an RGBA image to 1-bit transparency."""
    t = Image.new('RGBA',size(img))
    d = img.getdata()
    if type(d[0]) == int:
        return t
    if len(d[0]) != 4:
        return t
    newimg = []
    for pixel in d:
        r,g,b,a = pixel
        if a > threshold:
            newimg.append((r,g,b,255))
        else:
            newimg.append((r,g,b,0))
    t.putdata(newimg) # Put the new image together.
    return t

def loadSkinFromFile(path):
    """Loads a skin image from a file, defined by 'path'."""
    if not path.endswith('.png'):
        raise Exception('IncorrectExtensionException','Skin filename must end with .png')
    try:
        image = Image.open(path)
    except:
        raise Exception("SkinNotAvailableException","Skin image is not available.")
    if size(image) != (64,32):
        raise Exception("IncorrectDimensionsException","Skin image must be 64 pixels wide by 32 pixels tall.")
    return image


def loadSkinFromURL(url):
    """Loads a skin image from a URL, defined by 'url'."""
    try:
        remote = urllib.urlopen(url)
    except:
        raise Exception("SkinNotAvailableException","Skin image is not available.")
    local = StringIO(remote.read())
    image = Image.open(local)
    if size(image) != (64,32):
        raise Exception("IncorrectDimensionsException","Skin image must be 64 pixels wide by 32 pixels tall.")
    return image


def getHead(img):
    """Gets head data from a skin image."""
    tmp = Image.new('RGBA',(8,8),'white')
    x = img.copy()
    tmp.paste(x.crop((8,8,16,16)))
    if dim > 1:
        tmp = tmp.resize((dim * 8,dim * 8), Image.NEAREST)
    return tmp


def getHelmet(img):
    """Gets helmet data from a skin image."""
    tmp = Image.new('RGBA',(8,8))
    x = convert(img,1)
    pixels = x.crop((40,8,48,16))
    copy = False

    for pix in list(pixels.getdata()):
        if pix[3] <= 1:
            copy = True
            break;
    if copy == True:
        tmp.paste(pixels)
    if dim > 1:
        tmp = tmp.resize((dim*8,dim*8), Image.NEAREST)
    return tmp


def getCompleteHead(img):
    """Gets a complete head from a skin image."""
    tmp = Image.new('RGBA',(dim*8,dim*8))
    tmp.paste(getHead(img),(0,0))
    t = getHelmet(img)
    tmp.paste(t,(0,0),t)
    del t
    return tmp


def getBody(img):
    """Gets the front face of the body."""
    tmp = Image.new('RGBA',(8,12),"white")
    tmp.paste(img.crop((20,20,28,32)))
    tmp = tmp.resize((dim*8,dim*12), Image.NEAREST)
    return tmp


def getArms(img):
    """Gets the front face of the arms. Both arms are the same."""
    tmp = Image.new('RGBA',(4,12),"white")
    tmp.paste(img.crop((44,20,48,32)))
    tmp = tmp.resize((dim*4,dim*12), Image.NEAREST)
    return tmp


def getLegs(img):
    """Gets the front face of the legs. Both legs are the same."""
    tmp = Image.new('RGBA',(4,12),"white")
    tmp.paste(img.crop((4,20,8,32)))
    tmp = tmp.resize((dim*4,dim*12), Image.NEAREST)
    return tmp

def wholeBody(img):
    """Puts together all of the above in order to get a full body image."""
    tmp = Image.new('RGBA',(dim*16,dim*32))
    # Head
    tmp.paste(getCompleteHead(img),(dim*4,0))

    # Body
    tmp.paste(getBody(img),(dim*4,dim*8))

    # Arms
    t_arm = getArms(img)
    tmp.paste(t_arm,(0,dim*8))
    t_arm = t_arm.transpose(Image.FLIP_LEFT_RIGHT)
    tmp.paste(t_arm,(dim*12,dim*8))
    del t_arm

    # Legs
    t_leg = getLegs(img)
    tmp.paste(t_leg,(dim*4,dim*20))
    t_leg = t_leg.transpose(Image.FLIP_LEFT_RIGHT)
    tmp.paste(t_leg,(dim*8,dim*20))

    return tmp

def generateAvatar(img):
    """Generates a full avatar using all of the above."""
    d = dim*64
    tmp = Image.new('RGBA',(d+(2*dim),(d+(2*dim)))) # will be resized to half size afterward
    x = getCompleteHead(img)
    y = wholeBody(img)

    l,o = size(y)

    x = x.resize((d,d), Image.NEAREST)
    y = y.resize((l,o), Image.NEAREST)

    tmp.paste(y,(width(tmp)-(4*dim)-(dim*16),height(tmp)-(4*dim)-(dim*32)))
    tmp = tmp.resize((d,d), Image.NEAREST)

    x.paste(tmp,None,tmp)
    return x.resize((d/2,d/2), Image.NEAREST)

dim = 16
getCompleteHead(loadSkinFromURL('https://s3.amazonaws.com/MinecraftSkins/Notch.png')).save('herpin.png','PNG')