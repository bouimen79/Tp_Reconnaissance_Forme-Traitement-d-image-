import math
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import  numpy as np
from matplotlib import pyplot as plt
root = Tk()
root.configure(bg='gray17')
root.geometry("500x500")
root.title("Traitement d'Image")
scrollbar = Scrollbar(root)
scrollbar.pack( side = RIGHT, fill = Y )
#dicitionnaire of color
color={"nero":"#252726","orange":"#FF8700","darkorange":"#FE6101"}
navIcon=PhotoImage(file="icons8-menu-42.png")
closeIcon=PhotoImage(file="icons8-close-window-42.png")
topFrame = Frame(root, bg=color["orange"])
topFrame.pack(side="top", fill=X)
homeLabel = Label(topFrame, text="Image Processing", font="Bahnschrift 15", bg=color["orange"], fg="gray17", height=2, padx=20)
homeLabel.pack(side="right")
brandLabel = Label(root, text="Load \nImage", font="System 30", bg="gray17", fg="green")
brandLabel.place(x=100, y=250)
uploaded_img=Label(root)
uploaded_img.pack(pady=25)
# setting switch state:
btnState = False


def switch():
    global btnState
    if btnState is True:
        # create animated Navbar closing:
        for x in range(301):
            navRoot.place(x=-x, y=0)
            topFrame.update()
        # resetting widget colors:
        brandLabel.config(bg="gray17", fg="green")
        homeLabel.config(bg=color["orange"])
        topFrame.config(bg=color["orange"])
        root.config(bg="gray17")
        # turning button OFF:
        btnState = False
    else:
        # make root dim:
        brandLabel.config(bg=color["nero"], fg="#5F5A33")
        homeLabel.config(bg=color["nero"])
        topFrame.config(bg=color["nero"])
        root.config(bg=color["nero"])
        # created animated Navbar opening:
        for x in range(-300, 0):
            navRoot.place(x=x, y=0)
            topFrame.update()
        # turing button ON:
        btnState = True
#------------------------------------------Traitement de l'Image-------------------------------------------------------------------------------
def erosion(img,elm_struc): #-----------------------erosion---------------------------------------------------------------------------------------
    s=img.shape#la taille de limage exp (5)
    f=elm_struc.shape #la taille de l'element structurant
    img=img/255 #ecrire limage en binaire
    R=s[0]+f[0]-1
    C=s[1]+f[1]-1
    N=np.zeros((R,C))#crrer un tableau de 0
    for i in range(s[0]):
        for j in range(s[1]):
            N[i+1,j+1]=img[i,j]
    for i in range(s[0]):
        for j in range(s[1]):
            k=N[i:i+f[0],j:j+f[1]]
            result=(k==elm_struc) #si lelement structurant egale au pixel lirana fih
            final=np.all(result==True) #donc kml hadik la case eqal lelement structurant
            if final:
               img[i,j]=1 #en met 1
            else:
                img[i,j]=0 # sinon en met un 0 sa veut dire qui n'est pa eqal
    #cv2.imshow("Erosion Image",img)
    return img*255
def dilatation(img,elm_struc):#---------------------------------dilatation ---------------------
    s=img.shape
    f=elm_struc.shape
    img=img/255
    R=s[0]+f[0]-1
    C=s[1]+f[1]-1
    N=np.zeros((R,C))
    for i in range(s[0]):
        for j in range(s[1]):
            N[i+1,j+1]=img[i,j]
    for i in range(s[0]):
        for j in range(s[1]):
            k=N[i:i+f[0],j:j+f[1]]
            result=(k==elm_struc)#
            final=np.any(result==True) #au moin un pixel egale au element structurant .....
            if final:
                img[i,j]=1
            else:
                img[i,j]=0
    # cv2.imshow("Dilation Image",img)
    return img*255
def ouverture(bina,elm_struc): #------------------------------ouverture--------------------------
    o=erosion(bina,elm_struc)
    o2=dilatation(o,elm_struc)
    return o2
def fermeture(bina,elm_struc): #-------------------------------fermeture-----------------------------------------
    c = dilatation(bina, elm_struc)
    c2 = erosion(c, elm_struc)
    return c2
def change(path):
    img = ImageTk.PhotoImage(Image.open(path))
    uploaded_img.configure(image=img)
    uploaded_img.image = img
def operation_morpholgy(): #----------------------------------------Operation morphlogy--------------------------
    # telecharger limage depuis un fichier
    path=filedialog.askopenfilename(filetypes=(("jpeg files", "*.jpg"), ("gif files", "*.gif*"), ("png files", "*.png")))
    img1 = cv2.imread(path)
    #changement de limage to_binary --------
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    (thresh, bina) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    elm_struc = np.ones((4, 4), np.uint8)
    dial=dilatation(bina,elm_struc)
    eros=erosion(bina,elm_struc)
    contour=eros-bina #extraction de contour
    op=ouverture(bina,elm_struc) # appel au  fonction ouverture
    clos=fermeture(bina,elm_struc) # appel au fonction fermeture
    image=[bina,eros,dial,op,clos,contour] # list des resultat de tous les operation morphologie
    titles=['Image en Binaire','Erosion ','Dilation ','ouverture ','fermeture ','Contour d_Image']
    for i in range(6):
        plt.subplot(3,2,i+1)
        plt.imshow(image[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    change(path)
    plt.show()
#------------------------------fonction de lumunisoté _ convolution _redimonsionner _extraction de text _rotation -------------------------------
#------------------------------------Luminosité() luminositer---------------------------------------------
def Luminosité(bri,con):
    #telecharger limage depuis un fichier
    path = filedialog.askopenfilename(filetypes=(("jpeg files", "*.jpg"), ("gif files", "*.gif*"), ("png files", "*.png")))
    change(path)
    img = cv2.imread(path)
    diffcon = (100 - con)
    if diffcon <= 0.1: con=99.9
    arg = math.pi * (((con * con) / 20000) + (3 * con / 200)) / 4
    slope = 1 + (math.sin(arg) / math.cos(arg))
    if slope < 0: slope=0
    pivot = (100 - bri) / 200
    intcpbri = bri / 100
    intcpcon = pivot * (1 - slope)
    intercept = (intcpbri + intcpcon)
    # la pente et l'interception
    print(slope, intercept)
    # appliquer la pente et intercepter
    img = img/255.0
    out = slope * img + intercept
    out[out>1] = 1
    out[out<0] = 0
    cv2.imshow('OUT', out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # save output image
    out = 255.0 * out
    out = out.astype(int)
    cv2.imwrite('lena_bc_20_20.png', out)
bri =int(input("entrer la valeur de briallance :"))
con =int(input("entrer la valeur de conrast :"))

#----------------------------------------redimensionner------------------------------
def Redimensionner(x,y):
    #convertir image a une matrice
    path = filedialog.askopenfilename(
        filetypes=(("jpeg files", "*.jpg"), ("gif files", "*.gif*"), ("png files", "*.png")))
    change(path)
    image = np.array(Image.open(path))
    #image = np.array(Image.open("car.png"))
    height=image.shape[0]  #recupirer nombre de ligne
    width=image.shape[1]    #recupirer nombre de column
    #créer une matrice vide de zeros
    res=np.zeros((int(height*y),int(width*x),3),dtype="uint8")
    for i in range(int(height*y)):
        for j in range(int(width*x)):
            new_i=int(i/y)
            new_j=int(j/x)
            #bach may3adich 7odod ta3 image
            if (0 <= math.ceil(new_i) < height) and (0 <= math.ceil(new_j) < width):
                res[i,j]=image[new_i,new_j]
    pil_img=Image.fromarray((res).astype(np.uint8))                       # convertion tableau to image
    pil_img.save("rodime.png")
    pil_img.show()
x =int(input("entrer la valeur de X pour redimensionner :"))
y =int(input("entrer la valeur de Y pour redimensionner :"))

#--------------------------rotation(---------------------------------------------
def shear(angle,x,y):
    '''
    |1  -tan(𝜃/2) |  |1        0|  |1  -tan(𝜃/2) |
    |0      1     |  |sin(𝜃)   1|  |0      1     |
    '''
    # shear 1
    tangent=math.tan(angle/2)
    new_x=round(x-y*tangent)
    new_y=y
    #shear 2
    new_y=round(new_x*math.sin(angle)+new_y)      #puisqu'il n'y a pas de changement dans new_x selon la matrice de cisaillement
    #shear 3
    new_x=round(new_x-new_y*tangent)              #puisqu'il n'y a pas de changement dans new_y selon la matrice de cisaillement
    return new_y,new_x
def retate(angle):
    path = filedialog.askopenfilename(
        filetypes=(("jpeg files", "*.jpg"), ("gif files", "*.gif*"), ("png files", "*.png")))
    change(path)
    image = np.array(Image.open(path))             # Load the image


    # Définir les variables les plus courantes
    angle=math.radians(angle)                             #conversion de degrés en radians
    cosine=math.cos(angle)
    sine=math.sin(angle)
    height=image.shape[0]                                  #définir la hauteur de l'image
    width=image.shape[1]                                    #définir la largeur de l'image
    # Définir la hauteur et la largeur de la nouvelle image à former
    new_height  = round(abs(image.shape[0]*cosine)+abs(image.shape[1]*sine))+1
    new_width  = round(abs(image.shape[1]*cosine)+abs(image.shape[0]*sine))+1

    # définit une autre variable image des dimensions de new_height et new _column remplie de zéros
    output=np.zeros((new_height,new_width,image.shape[2]))
    image_copy=output.copy()
    # Trouver le centre de l'image autour duquel nous devons faire pivoter l'image
    original_centre_height   = round(((image.shape[0]+1)/2)-1)    #par rapport à l'image originale
    original_centre_width    = round(((image.shape[1]+1)/2)-1)    #par rapport à l'image originale

    # Trouver le centre de la nouvelle image qui sera obtenue
    new_centre_height= round(((new_height+1)/2)-1)        #par rapport à la nouvelle image
    new_centre_width= round(((new_width+1)/2)-1)          #par rapport à la nouvelle image
    for i in range(height):
        for j in range(width):
            #coordonnées du pixel par rapport au centre de l'image originale
            y=image.shape[0]-1-i-original_centre_height
            x=image.shape[1]-1-j-original_centre_width
            #Appliquer la transformation de cisaillement
            new_y,new_x=shear(angle,x,y)
            '''puisque l'image sera tournée, le centre changera aussi,
                            donc pour s'adapter à cela, nous devrons changer new_x et new_y par rapport au nouveau centre'''
            new_y=new_centre_height-new_y
            new_x=new_centre_width-new_x
            output[new_y,new_x,:]=image[i,j,:]                          #writing the pixels to the new destination in the output image
    pil_img=Image.fromarray((output).astype(np.uint8))                       # converting array to image
    pil_img.show()
angle=-int(input("Enter the angle : "))
#-------------------------------convolution----------------------------------------------------------
def somme(M):
    s = 0
    for i in range(len(M)):
        for j in range(len(M[0])):
            s += M[i][j]
    return s
def calcul_masque(img, index_I, index_J, width, height, masque):
    masque_c_i = len(masque) // 2
    masque_c_j = len(masque[0]) // 2
    #d=[-1,0,1]if masque=3x3d=[-2,-1,0,1,2]if masque=5x5
    v = range(math.ceil(-len(masque) / 2), math.ceil(len(masque) / 2))
    #initialiser nouvelle valeur de notre pixel
    new = [0, 0, 0]
    #parcourir d pour multiplier tous les voisins
    for i in v:
        for j in v:
            # l= position de notre pixel qui nous veux calculer
            p = img[(index_I + i) % width, (index_J + j) % height]
            new[0] += p[0] * masque[masque_c_i - i][masque_c_j - j]
            new[1] += p[1] * masque[masque_c_i - i][masque_c_j - j]
            new[2] += p[2] * masque[masque_c_i - i][masque_c_j - j]
    s = somme(masque)
    return new[0] // s, new[1] // s, new[2] // s
def convolution( masque):
    path = filedialog.askopenfilename(
        filetypes=(("jpeg files", "*.jpg"), ("gif files", "*.gif*"), ("png files", "*.png")))
    change(path)
    image = Image.open(path)
    width, height = image.size
    img = image.load()
    imgRES = Image.new('RGB', (width, height))
    res = imgRES.load()
    for i in range(width):
        for j in range(height):
            res[i, j] = calcul_masque(img, i, j, width, height, masque)
    imgRES.show()
masque = [[1, 1, 1],
           [1, 1, 1],
           [1, 1, 1]]
#--------------------------extract text from image -------------------------------------------------------------------------------------

def column(array, i):
    return [x[i] for x in array]
def to_image(data):
    width, height = len(data), len(data[0])
    imgRES = Image.new('RGB', (width, height))
    res = imgRES.load()
    for i in range(width):
        for j in range(height):
            if data[i][j] == 0:
                res[i, j] = (255, 255, 255)
            else:
                res[i, j] = (0, 0, 0)
    return imgRES

def show_images_b(data, axis='on', titles=[]):
    if len(titles) == 0: titles = ['' for _ in range(len(data))]
    fig = plt.figure()
    for i in range(len(data)):
        fig.add_subplot(math.ceil(len(data) / math.ceil(math.sqrt(len(data)))), math.ceil(math.sqrt(len(data))), i + 1)
        plt.imshow(to_image(data[i]))
        plt.axis(axis)
        plt.title(titles[i])
    fig.tight_layout()
    plt.show()
def to_binary():
    path = filedialog.askopenfilename(
        filetypes=(("jpeg files", "*.jpg"), ("gif files", "*.gif*"), ("png files", "*.png")))
    change(path)
    image = Image.open(path)
    width, height = image.size
    image = image.load()
    data = [[None for _ in range(height)] for _ in range(width)]
    for i in range(width):
        for j in range(height):
            if (0.2989 * image[i, j][0]
                + 0.5871 * image[i, j][1]
                + 0.1140 * image[i, j][2]) > 110:
                data[i][j] = 0
            else:
                data[i][j] = 1
    return data
def extr_column(data):# extractioon tous les coolones
    res = []
    col = []
    for line in data:
        for c in line:
            if 1 in c:
                col.append(c)
            else:
                if len(col) != 0:
                    res.append(col)
                    col = []
    return res

def extr_line(data):# extraction tous les ligne qui contient des pixel en noir
    res = []
    line = []
    for i in range(len(data[0])):
        l = column(data, i)
        if 1 in l:
            line.append(l)
        else:
            if len(line) != 0:
                line_inv = []
                for c in range(len(line[0])):
                    line_inv.append(column(line, c))
                res.append(line_inv)
                line = []
    return res


def extract_char(data):
    return extr_column(extr_line(data))


#-----------------------------------------histogram -----------------------------------------------------------
def histog_img():
    path = filedialog.askopenfilename(
        filetypes=(("jpeg files", "*.jpg"), ("gif files", "*.gif*"), ("png files", "*.png")))
    change(path)
    img=cv2.imread(path)
    #recupirer les lignes et les colones
    s=img.shape
    #rendre image gris
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow("binary",img_gray)
    cv2.waitKey(0)
    h=np.zeros(shape=(256,1))
    for i in range(s[0]):
        for j in range(s[1]):
            k=img_gray[i,j]
            h[k,0]=h[k,0]+1
    plt.figure(figsize=[10,8])
    plt.plot(h)
    plt.xlabel('couleur',fontsize=15)
    plt.ylabel('pixels',fontsize=15)
    plt.show()

#--------------------------------------boutoon de linterface ---------------------------------------------------------------------------
# Navbar button:
navbarBtn = Button(topFrame, image=navIcon, bg=color["orange"], activebackground=color["orange"], bd=0, padx=20, command=switch)
navbarBtn.place(x=10, y=10)
# setting Navbar frame:
navRoot = Frame(root, bg="gray17", height=1000, width=300)
navRoot.place(x=-300, y=0)
Label(navRoot, font="Bahnschrift 15", bg=color["orange"], fg="black", height=2, width=300, padx=20).place(x=0, y=0)
# set y-coordinate of Navbar widgets:
y = 80
# option in the navbar:
# Navbar Option Buttons:

Button(navRoot, command=lambda :Luminosité(bri,con),text="Luminosité", font="BahnschriftLight 15", bg="gray17", fg=color["orange"], activebackground="gray17", activeforeground="green", bd=0).place(x=25, y=160)
Button(navRoot,command=lambda :retate(angle),text="Rotation", font="BahnschriftLight 15", bg="gray17", fg=color["orange"], activebackground="gray17", activeforeground="green", bd=0).place(x=25, y=200)
Button(navRoot,command=lambda :Redimensionner(x,y),text="Redimensionner", font="BahnschriftLight 15", bg="gray17", fg=color["orange"], activebackground="gray17", activeforeground="green", bd=0).place(x=25, y=240)
Button(navRoot,command=operation_morpholgy ,text=" Operation_Morphogy", font="BahnschriftLight 15", bg="gray17", fg=color["orange"], activebackground="gray17", activeforeground="green", bd=0).place(x=25, y=280)
Button(navRoot,command=lambda :convolution(masque) ,text="Convolution", font="BahnschriftLight 15", bg="gray17", fg=color["orange"], activebackground="gray17", activeforeground="green", bd=0).place(x=25, y=320)
Button(navRoot,command=lambda :show_images_b(extract_char(to_binary()), 'on') ,text="Extraction Text", font="BahnschriftLight 15", bg="gray17", fg=color["orange"], activebackground="gray17", activeforeground="green", bd=0).place(x=25, y=360)
Button(navRoot,command=histog_img ,text="histograme ", font="BahnschriftLight 15", bg="gray17", fg=color["orange"], activebackground="gray17", activeforeground="green", bd=0).place(x=25, y=400)
# Navbar Close Button:
closeBtn = Button(navRoot, image=closeIcon, bg=color["orange"], activebackground=color["orange"], bd=0, command=switch)
closeBtn.place(x=250, y=10)

root.mainloop()
