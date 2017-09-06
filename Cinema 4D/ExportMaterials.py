import c4d, os
from c4d import gui, documents, plugins, utils, storage
#Welcome to the world of Python

def hook(dict):
    a = 2

#def cooKColor(bakeSettings)

def shadertree(shader):
    # Loop through the BaseList
    while(shader):
         
        # This is where you do stuff
       # print shader.GetName()
        # If it's a bitmap, we'll look at the filename
        #print(shader.GetRenderInfo())
        if shader.GetType() == c4d.Xbitmap:
            filename = shader[c4d.BITMAPSHADER_FILENAME]
            #print filename
            #print(c4d.storage.LoadDialog(c4d.FILESELECTTYPE_IMAGES, filename))
            # for instance we can set the filename to just the file part
            filename = doc.GetDocumentPath() +"\\tex\\" + filename
            print(filename)
            #print(filename)
            #print(doc.GetDocumentPath())
            bmp = c4d.bitmaps.BaseBitmap()
            bmp.InitWith(filename)[0]
            x, y = bmp.GetSize()
            print("x:" + str(x))
            if x == 0:
                x = 512
                y = 512
            if x > 4000 or y > 4000:
                x = x / 2
                y = y / 2
            
            return x,y
        if shader.GetType() == c4d.Xtiles:
            print("hey")   
            
            #shader[c4d.BITMAPSHADER_FILENAME] = filename
         
        # Check for child shaders & recurse
        if shader.GetDown(): shadertree(shader.GetDown())
        # Get the Next Shader
        shader = shader.GetNext()

def bake(currentTexture, currentUvw, bakeSettings, filename, size):
    
    bitmap = c4d.bitmaps.MultipassBitmap(size[0],size[1], c4d.COLORMODE_ARGB)
    #if type(bitmap.GetLayers(c4d.MPB_GETLAYERS_0)) == c4d.bitmaps.MultipassBitmap:
    bitmap.AddAlpha(bitmap, c4d.COLORMODE_ALPHA)
   # bitmap.Save("Johny", c4d.FILTER_JPG)
    baseDoc =  c4d.utils.InitBakeTexture(doc, currentTexture, currentUvw, None,bakeSettings, None)
    print(baseDoc[1])
    print(c4d.BAKE_TEX_ERR_WRONG_BITMAP)
    print("f:"+filename )
    filename = doc.GetDocumentPath() + "/tex/"  + filename + ".png"
    print( c4d.utils.BakeTexture(baseDoc[0], bakeSettings,bitmap, None,hook ))
    print("f:"+filename )
    #bitmap.AddAlpha(bitmap.GetLayers(c4d.MPB_GETLAYERS_0), c4d.COLORMODE_ALPHA)
    print(bitmap.Save(filename, c4d.FILTER_PNG, c4d.BaseContainer(),c4d.SAVEBIT_ALPHA))
  
    c4d.bitmaps.ShowBitmap(bitmap)

def setBakeSettings(material, f):
 
    shd = material.GetFirstShader()
    size = shadertree(shd)
    hasTexture = True
    print(size)
   
    NewObject = c4d.BaseObject(c4d.Ocube)
    tag = NewObject.MakeTag(c4d.Ttexture)
    tag.SetMaterial(material)
    NewObject.MakeTag(c4d.Tuvw)
    #tag[c4d.TEXTURETAG_MATERIAL] = currentTexture.GetMaterial()
   # doc.AddUndo(c4d.UNDOTYPE_NEW, tag)
    doc.InsertObject(NewObject)           # Insert object in document
    c4d.EventAdd()
    currentUvw = NewObject.GetTag(c4d.Tuvw)
    currentTexture = NewObject.GetTag(c4d.Ttexture)
    currentMat = currentTexture.GetMaterial()
    bakeSettings = c4d.BaseContainer()
    #bakeSettings[c4d.BAKE_TEX_WIDTH] = 512
    #bakeSettings[c4d.BAKE_TEX_HEIGHT] = 512
    #bakeSettings[c4d.BAKE_TEX_PIXELBORDER] = 1
    #bakeSettings[c4d.BAKE_TEX_CONTINUE_UV] = False
    if shd is None or size is None:
        if shd is None:
            hasTexture = False
        size = 256,256
    print(size)
    bakeSettings.SetLong(c4d.BAKE_TEX_WIDTH, size[0])
    bakeSettings.SetLong(c4d.BAKE_TEX_HEIGHT, size[1])
    bakeSettings.SetLong(c4d.BAKE_TEX_PIXELBORDER, 0)
    bakeSettings.SetBool(c4d.BAKE_TEX_CONTINUE_UV, False)
    bakeSettings.SetVector(c4d.BAKE_TEX_FILL_COLOR, c4d.Vector(1.0))
    bakeSettings.SetLong(c4d.BAKE_TEX_SUPERSAMPLING, 0)
    bakeSettings.SetFloat(c4d.BAKE_TEX_UV_LEFT, 0.0)
    bakeSettings.SetFloat(c4d.BAKE_TEX_UV_RIGHT, 1.0)
    bakeSettings.SetFloat(c4d.BAKE_TEX_UV_TOP, 0.0)
    bakeSettings.SetFloat(c4d.BAKE_TEX_UV_BOTTOM, 1.0)
   
    #bakeSettings[c4d.BAKE_TEX_SUPERSAMPLING] = 0
    #bakeSettings[c4d.BAKE_TEX_FILL_COLOR] = c4d.Vector(1)
    #bakeSettings[c4d.BAKE_TEX_USE_BUMP] = False
    #bakeSettings[c4d.BAKE_TEX_USE_CAMERA_VECTOR] = False
    #bakeSettings[c4d.BAKE_TEX_AUTO_SIZE] = False
    #bakeSettings[c4d.BAKE_TEX_NO_GI] = False
    #bakeSettings[c4d.BAKE_TEX_GENERATE_UNDO] = False
    #bakeSettings[c4d.BAKE_TEX_PREVIEW] = False
    #bakeSettings[c4d.BAKE_TEX_COLOR] = True
    #bakeSettings[c4d.BAKE_TEX_UV_LEFT] = 0.0
    #bakeSettings[c4d.BAKE_TEX_UV_RIGHT] = 1.0
    #bakeSettings[c4d.BAKE_TEX_UV_TOP] = 0.0
    #bakeSettings[c4d.BAKE_TEX_UV_BOTTOM] = 1.0
   # bakeSettings[c4d.BAKE_TEX_OPTIMAL_MAPPING] = c4d.BAKE_TEX_OPTIMAL_MAPPING_CUBIC
    
    #BAKE_TEX_NO_INIT_BITMAP
    bakeSettings.SetBool(c4d.BAKE_TEX_USE_CAMERA_VECTOR, False)
    bakeSettings.SetBool(c4d.BAKE_TEX_USE_POLYSELECTION, False)
    bakeSettings.SetBool(c4d.BAKE_TEX_AMBIENT_OCCLUSION, False)
   # if currentMat.GetChannelState(c4d.CHANNEL_NORMAL) == True:
   
    #bakeSettings.SetBool(c4d.BAKE_TEX_NORMAL, True);
    #fileName = currentMat.GetName() + "NORMAL"
    #bake(currentTexture, currentUvw, bakeSettings, fileName,size)
    #bakeSettings.SetBool(c4d.BAKE_TEX_NORMAL, False);
    #
   
    #shader = currentMat[c4d.MATERIAL_ALPHA_SHADER]
    #if shader is None:
        #print("zz")
   # irs = c4d.modules.render.InitRenderStruct()
    #if shader.InitRender(irs)==c4d.INITRENDERRESULT_OK:
    #bitmap = shader.GetBitmap()
    #shader.FreeRender()
    #if bitmap is not None:
        #bitmaps.ShowBitmap(bitmap)
        #print("xx")
  
    f.write("MATERIAL:" + currentMat.GetName()  +  "\n")
    print (currentMat.GetName())
    print (type(currentMat))
    if type(currentMat) == c4d.BaseMaterial:
        return;
    if currentMat.GetChannelState(c4d.CHANNEL_ALPHA) == True:
        f.write("ALPHA:\n")
        bakeSettings.SetBool(c4d.BAKE_TEX_ALPHA, True);
        fileName = currentMat.GetName() +  "ALPHA"
        f.write("Name:" + fileName + "\n")
        bake(currentTexture, currentUvw, bakeSettings, fileName,size)
        bakeSettings.SetBool(c4d.BAKE_TEX_ALPHA, False);
   
    if currentMat.GetChannelState(c4d.CHANNEL_COLOR) == True and hasTexture == True:
        bakeSettings.SetBool(c4d.BAKE_TEX_COLOR, True);
      
        fileName = currentMat.GetName() + "COLOR" 
        f.write("COLOR:" + "\n")
        f.write("Name:" + fileName + "\n")
        if hasTexture == True:
            bake(currentTexture, currentUvw, bakeSettings, fileName,size)
        f.write("ValueColor:" + str(currentMat.GetAverageColor(c4d.CHANNEL_COLOR)) + "\n")
        bakeSettings.SetBool(c4d.BAKE_TEX_COLOR, False);  
        
    if currentMat.GetChannelState(c4d.CHANNEL_REFLECTION) == True: 
        f.write("REFLECTION:" + "\n")
        f.write("Value:0.7" + "\n")
        print("Tuple:" + str(currentMat.GetReflectionPrimaryLayers()[0]))

    if currentMat.GetChannelState(c4d.CHANNEL_BUMP) == True:
        bakeSettings.SetBool(c4d.BAKE_TEX_BUMP, True);
        fileName = currentMat.GetName()  +  "BUMP" 
        f.write("BUMP:"+ "\n")
        f.write("Name:" + fileName+ "\n")
        bake(currentTexture, currentUvw, bakeSettings, fileName,size)
        bakeSettings.SetBool(c4d.BAKE_TEX_BUMP, False);     
     
    if currentMat.GetChannelState(c4d.CHANNEL_DIFFUSION) == True:
        bakeSettings.SetBool(c4d.BAKE_TEX_DIFFUSION, True);
        fileName = currentMat.GetName()  +  "DIFFUSION" 
        f.write("DIFFUSION:"+ "\n")
        f.write("Name:" + fileName+ "\n")
        bake(currentTexture, currentUvw, bakeSettings, fileName,size)
        bakeSettings.SetBool(c4d.BAKE_TEX_DIFFUSION, False);
        
    if currentMat.GetChannelState(c4d.CHANNEL_LUMINANCE) == True:
        bakeSettings.SetBool(c4d.BAKE_TEX_LUMINANCE, True);
        fileName = currentMat.GetName()  +  "LUMINANCE" 
        f.write("LUMINANCE:"+ "\n")
        f.write("Name:" + fileName+ "\n")
        bake(currentTexture, currentUvw, bakeSettings, fileName,size)
        bakeSettings.SetBool(c4d.BAKE_TEX_LUMINANCE, False);     
     #if currentMat.GetChannelState(c4d.CHANNEL_REFLECTION) == True:
        #f.write("REFLECTION:\n")
        #bakeSettings.SetBool(c4d.BAKE_TEX_REFLECTION, True);
        #fileName = currentMat.GetName() + stringCount +  "REFLECTION"
        #f.write("Name:" + fileName + "\n")
        #f.write("Tile:" + str(x) + "," +  str(y) + "\n")
        #bake(currentTexture, currentUvw, bakeSettings, fileName,size)
        bakeSettings.SetBool(c4d.BAKE_TEX_REFLECTION, False);
    #bakeSettings.SetBool(c4d.BAKE_TEX_DIFFUSION, False);
    #bakeSettings.SetBool(c4d.BAKE_TEX_LUMINANCE, False);
    bakeSettings.SetBool(c4d.BAKE_TEX_ALPHA, False);
    #bakeSettings.SetBool(c4d.BAKE_TEX_UVMAP, False);
    #bakeSettings.SetBool(c4d.BAKE_TEX_ILLUMINATION, False);
    bakeSettings.SetBool(c4d.BAKE_TEX_SHADOWS, False);

    bakeSettings.SetBool(c4d.BAKE_TEX_BUMP, False);
    bakeSettings.SetBool(c4d.BAKE_TEX_TRANSPARENCY, False);
    bakeSettings.SetBool(c4d.BAKE_TEX_UVMAP, False);
    bakeSettings.SetBool(c4d.BAKE_TEX_REFLECTION, False);
    
    NewObject.Remove()


    #######
    #bakeSettings.SetBool(c4d.BAKE_TEX_NO_GI, False);
    #bakeSettings.SetBool(c4d.BAKE_TEX_COLOR_ILLUM, False);
    #bakeSettings.SetBool(c4d.BAKE_TEX_COLOR_SHADOWS, False);
    ###


   
    
def main():
   
    f = open("C:\Users\labsf\Desktop\info2.txt","w+")
    mats = doc.GetMaterials()
   
    for x in mats:
        setBakeSettings(x,f)
      
                              
    f.close()
    

if __name__=='__main__':
    main()
