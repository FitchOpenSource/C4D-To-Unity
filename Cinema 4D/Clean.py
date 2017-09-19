import c4d
from c4d import gui, documents
#Welcome to the world of Python

def findNameMaterial(string, materials, cnt):
    
    cnt = cnt + 1
    string  = string + "_" + str(cnt)
    if materials.count(string) == 0:
        return string
    else:
        string = findNameMaterial(string,materials,cnt)
    return string


#Create a unique name for the materials and remove unorthodox characters

def cleanMaterials():
    mats = doc.GetMaterials()
    materials = []
    for x in mats:
        string = x.GetName()
        if string.find(".") != -1:
            string =  x.GetName()
            string = string.replace(".", "")
            string = string.replace("*", "")
        if materials.count(string) == 0:
            materials.append(string)
        else:
            string = findNameMaterial(string, materials,0)
            materials.append(string)
        x.SetName(string) 
    c4d.documents.SetActiveDocument(doc)

#def findNameObject(string, objects, cnt):
#    
    #cnt = cnt + 1
    #tmp = string;
    #string  = string + "_" + str(cnt)
    #if objects.count(string) == 0:
        #return string
    #else:
        #string = findNameObject(tmp,objects,cnt)
    #return string

def iterateChildren(obj, objects):
    #cleanObjects(obj, objects)
    CleanTags(obj)
    for child in obj.GetChildren():
        iterateChildren(child, objects)

def CleanTags(obj):
    doc.SetActiveObject(obj)
    lists = []
    lists.append(obj)
   
    listTags = obj.GetTags()
    listMultipleTextureTags = []
   
    
    # Make current Object Editable
    
    c4d.CallCommand(12236)
    c4d.documents.SetActiveDocument(doc)
    
    # Null Object are ignored
    
    if obj.GetType() == c4d.Onull:
        return
    
####################

    #Remove Duplicated texture tags (keeps Polygon Selection)
    
    hasUVWLock = False 
    for t in listTags:
        if type(t) == c4d.TextureTag and t.GetMaterial() is not None:
            selection = t[c4d.TEXTURETAG_RESTRICTION]
            if selection == "":
                listMultipleTextureTags.append(t)
        if  type(t) == c4d.TextureTag and t.GetMaterial() is None:
            t.Remove()
    increment = 0
    tag = None
    for tTags in  listMultipleTextureTags:
        selection =  listMultipleTextureTags[increment][c4d.TEXTURETAG_RESTRICTION]
        if len(listMultipleTextureTags) !=  (increment + 1):
           listMultipleTextureTags[increment].Remove()
        tag = listMultipleTextureTags[increment]
        increment = increment + 1
      
####################  
    
    
    #if uvw tag is locked(UVWTAG_LOCK =  true) then we don't erase it
    
    UVWtag = obj.GetTag(c4d.Tuvw)
    if UVWtag is not None and (tag is None or tag[c4d.TEXTURETAG_PROJECTION] == 6):
        obj.GetTag(c4d.Tuvw)[c4d.UVWTAG_LOCK] = True
        c4d.EventAdd()
   
   
    listTags = obj.GetTags()
    for t in listTags:
         if type(t) == c4d.UVWTag:
            if t[c4d.UVWTAG_LOCK] == False:
                t.Remove()
            else:
                hasUVWLock = True
    
    
    # Generate 2 UVW tags one for texture and second for lighting
    
    if tag is None or tag[c4d.TEXTURETAG_PROJECTION] == 6 or UVWtag is None:
        doc.SetActiveObject(obj)
        if hasUVWLock == False:
            
            # Tags menu, UVW tags -> set from projection command
            
            c4d.CallCommand(1030000, 1030000)
            
            doc.SetActiveObject(obj)  
            if obj.GetTag(c4d.Tuvw) is not None:
                obj.GetTag(c4d.Tuvw)[c4d.UVWTAG_LOCK] = True
        doc.SetActiveObject(obj)  
        
         # Tags menu, UVW tags -> set from projection command
        
        c4d.CallCommand(1030000, 1030000)      
    else:
        doc.SetActiveTag(tag)
        
        # Tags menu, Generate UVW cordinates (this is in case texture tags projection is not set to UVW mapping )
         
        c4d.CallCommand(12235, 12235)
        tag[c4d.TEXTURETAG_TILE]=True
        obj.GetTag(c4d.Tuvw)[c4d.UVWTAG_LOCK] = True
        doc.SetActiveObject(obj)
        
         # Tags menu, UVW tags -> set from projection command
         
        c4d.CallCommand(1030000, 1030000)
    c4d.documents.SetActiveDocument(doc)
    Ttag = obj.GetTag(c4d.Ttexture)
    if Ttag is not None:
        obj.InsertTag(Ttag, None)
 
# Create a Unique name for the material (unity needs a unique name for materials)   

#def cleanObjects(x,objects):
    #string = x.GetName()
    #if string.find(".") != -1:
        #string = string.replace(".", "")
    #if objects.count(string) == 0:
        #objects.append(string)
    #else:
        #string = findNameObject(string, objects,0)
        #objects.append(string)
    #x.SetName(string) 
    #c4d.documents.SetActiveDocument(doc)


#Remove Invisble Objects

def iterateChildrenInvisble(obj):
    removeInvisbleObjects(obj)
    for child in obj.GetChildren():
        iterateChildrenInvisble(child)

def removeInvisbleObjects(obj):
    
    # if object is Invisible in Editor and Render delete it
    
    if obj.GetEditorMode()== 1 and  obj.GetRenderMode()== 1:
        obj.Remove()
  
####################
  
  
def main():
    
    #Remove Invisble Objects
    
    for obj in doc.GetObjects():
        iterateChildrenInvisble(obj)
    
    #Create a unique name for the materials and remove unorthodox characters
    
    cleanMaterials()
    
    #Add UVW tags (one for texture and other on for light)and Removed usless Texture tags
    objects = []
    for obj in doc.GetObjects():
        iterateChildren(obj, objects)
    print("Done")
    

if __name__=='__main__':
    main()
