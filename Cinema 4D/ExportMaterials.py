import c4d, os
from c4d import gui, documents, plugins, utils, storage
from c4d.threading import C4DThread
#Welcome to the world of Python



def hook(dict):
    a = 2

#def cooKColor(bakeSettings)

def shadertree(shader):
    
    # Loop through the BaseList
    
    while(shader):
         
        # This is where you do stuff
        # If it's a bitmap, we'll look at the filename
       
        if shader.GetType() == c4d.Xbitmap:
            filename = shader[c4d.BITMAPSHADER_FILENAME]
            
            # for instance we can set the filename to just the file part
           
            filename = doc.GetDocumentPath() +"\\tex\\" + filename
            bmp = c4d.bitmaps.BaseBitmap()
            bmp.InitWith(filename)[0]
            x, y = bmp.GetSize()
            if x == 0:
                x = 512
                y = 512
            if x > 4000 or y > 4000:
                x = x / 2
                y = y / 2
            
            return x,y
        
            
         
        if shader.GetDown(): 
            shadertree(shader.GetDown())
        # Get the Next Shader
        shader = shader.GetNext()

def bake(currentTexture, currentUvw, bakeSettings, filename, size):
    #Allocate memory for image
    bitmap = c4d.bitmaps.MultipassBitmap(size[0], size[1],  c4d.COLORMODE_ARGB)
    
    #Initialise bake 
    baseDoc =  c4d.utils.InitBakeTexture(doc, currentTexture, currentUvw, None,bakeSettings, None)
    
    #Location of Image file
    filename = doc.GetDocumentPath() + "/tex/"  + filename + ".png"
    thread = c4d.threading.GeGetCurrentThread()
    #Bake texture
    c4d.utils.BakeTexture(baseDoc[0], bakeSettings, bitmap, thread,hook)
    
    #Save image
    bitmap.Save(filename, c4d.FILTER_PNG, c4d.BaseContainer(),c4d.SAVEBIT_ALPHA)
    
    #Display Image
    #c4d.bitmaps.ShowBitmap(bitmap)
    return filename

def setBakeSettings(material):
    
    #Get size of texture image
    
    shd = material.GetFirstShader()
    size = shadertree(shd)
    hasTexture = True
  
    # Create a simple object to bake (complex objects have wierd texture mapping)
    NewObject = c4d.BaseObject(c4d.Ocube)
    
    # Add texture tag
    tag = NewObject.MakeTag(c4d.Ttexture)
    tag.SetMaterial(material)
    # Add uvw tag
    NewObject.MakeTag(c4d.Tuvw)
    doc.InsertObject(NewObject)           
    # Insert object in document
    c4d.EventAdd()
    
    currentUvw = NewObject.GetTag(c4d.Tuvw)
    currentTexture = NewObject.GetTag(c4d.Ttexture)
    currentMat = currentTexture.GetMaterial()
    
    bakeSettings = c4d.BaseContainer()
    
    # if texture channel is not using an image then set default size (ex:noise has no image)
    if shd is None or size is None:
        if shd is None:
            hasTexture = False
        size = 1024,1024
    
    #Default parameters for baking texture    
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
   
    bakeSettings.SetBool(c4d.BAKE_TEX_USE_CAMERA_VECTOR, False)
    bakeSettings.SetBool(c4d.BAKE_TEX_USE_POLYSELECTION, False)
    bakeSettings.SetBool(c4d.BAKE_TEX_AMBIENT_OCCLUSION, False)

    #If material is primitive, remove it
    if type(currentMat) == c4d.BaseMaterial:
        NewObject.Remove()
        return;
    
    #Bake Alpha channel
    if currentMat.GetChannelState(c4d.CHANNEL_ALPHA) == True:
        bakeSettings.SetBool(c4d.BAKE_TEX_ALPHA, True);
        bakeSettings.SetBool(c4d.BAKE_TEX_NO_INIT_BITMAP, False)
       
        #Invert option in the alpha channel
        if currentMat[c4d.MATERIAL_ALPHA_INVERT] == False:
            fileName = currentMat.GetName() +  "ALPHA"
        else:
            fileName = currentMat.GetName() +  "INVERTALPHA"
        
        #Replace old image by new baked image
        filePath = bake(currentTexture, currentUvw, bakeSettings, fileName,size)
        sha = c4d.BaseList2D(c4d.Xbitmap)
        sha[c4d.BITMAPSHADER_FILENAME]  = filePath
        currentMat.InsertShader( sha )
        currentMat[c4d.MATERIAL_ALPHA_SHADER]  = sha
        bakeSettings.SetBool(c4d.BAKE_TEX_ALPHA, False);
        
    
    #Bake Color channel    
    if currentMat.GetChannelState(c4d.CHANNEL_COLOR) == True and hasTexture == True:
        bakeSettings.SetBool(c4d.BAKE_TEX_COLOR, True);
        fileName = currentMat.GetName() + "COLOR" 
        if hasTexture == True:
            #Replace old image by new baked image
            filePath = bake(currentTexture, currentUvw, bakeSettings, fileName,size)
            sha = c4d.BaseList2D(c4d.Xbitmap)
            sha[c4d.BITMAPSHADER_FILENAME]  = filePath
            currentMat.InsertShader( sha )
            currentMat[c4d.MATERIAL_COLOR_SHADER]  = sha
        bakeSettings.SetBool(c4d.BAKE_TEX_COLOR, False);  
        
    #Bake Bump channel
    if currentMat.GetChannelState(c4d.CHANNEL_BUMP) == True:
        bakeSettings.SetBool(c4d.BAKE_TEX_BUMP, True);
        fileName = currentMat.GetName()  +  "BUMP" 
        
        #Replace old image by new baked image
        filePath = bake(currentTexture, currentUvw, bakeSettings, fileName,size)
        sha = c4d.BaseList2D(c4d.Xbitmap)
        sha[c4d.BITMAPSHADER_FILENAME]  = filePath
        currentMat.InsertShader( sha )
        currentMat[c4d.MATERIAL_BUMP_SHADER]  = sha
        bakeSettings.SetBool(c4d.BAKE_TEX_BUMP, False);     
    
    #Bake Diffusion channel 
    if currentMat.GetChannelState(c4d.CHANNEL_DIFFUSION) == True:
        bakeSettings.SetBool(c4d.BAKE_TEX_DIFFUSION, True);
        fileName = currentMat.GetName()  +  "DIFFUSION" 
        
        #Replace old image by new baked image
        filePath = bake(currentTexture, currentUvw, bakeSettings, fileName,size)
        sha = c4d.BaseList2D(c4d.Xbitmap)
        sha[c4d.BITMAPSHADER_FILENAME]  = filePath
        currentMat.InsertShader( sha )
        currentMat[c4d.MATERIAL_DIFFUSION_SHADER]  = sha
        bakeSettings.SetBool(c4d.BAKE_TEX_DIFFUSION, False);
    
    #Bake Luminance channel     
    if currentMat.GetChannelState(c4d.CHANNEL_LUMINANCE) == True:
        bakeSettings.SetBool(c4d.BAKE_TEX_LUMINANCE, True);
        fileName = currentMat.GetName()  +  "LUMINANCE"
        
        #Replace old image by new baked image     
        filePath = bake(currentTexture, currentUvw, bakeSettings, fileName,size)
        sha = c4d.BaseList2D(c4d.Xbitmap)
        sha[c4d.BITMAPSHADER_FILENAME]  = filePath
        currentMat.InsertShader( sha )
        currentMat[c4d.MATERIAL_LUMINANCE_SHADER]  = sha
        bakeSettings.SetBool(c4d.BAKE_TEX_LUMINANCE, False);     
    
   
    # Remove simple object used for baking
    NewObject.Remove()


# Thread
class UserThread(C4DThread):
  def Main(self):
    mats = doc.GetMaterials()
    countMaterial = 0;
    for x in mats:
        print(str(countMaterial) + "/" + str(len(mats)))
        setBakeSettings(x)
        countMaterial = countMaterial + 1
    pass                                
    print("Done")
    

thread = UserThread()
thread.Start()

