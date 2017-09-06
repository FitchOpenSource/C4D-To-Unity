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

def cleanMaterials():
    mats = doc.GetMaterials()
    materials = []
    for x in mats:
        string = x.GetName()
        if string.find(".") != -1:
            string =  x.GetName()
            string = string.replace(".", "")
        if materials.count(string) == 0:
            materials.append(string)
        else:
            string = findNameMaterial(string, materials,0)
            materials.append(string)
        x.SetName(string) 
    c4d.documents.SetActiveDocument(doc)

def findNameObject(string, objects, cnt):
    
    cnt = cnt + 1
    tmp = string;
    string  = string + "_" + str(cnt)
    if objects.count(string) == 0:
        return string
    else:
        string = findNameObject(tmp,objects,cnt)
    return string

def iterateChildren(obj, objects):
    #cleanObjects(obj, objects)
    CleanTags(obj)
    for child in obj.GetChildren():
        iterateChildren(child, objects)

def CleanTags(obj):
    listTags = obj.GetTags()
    listMultipleTextureTags = []
    for t in listTags:
        if type(t) == c4d.TextureTag and t.GetMaterial() is not None:
            selection = t[c4d.TEXTURETAG_RESTRICTION]
            if selection == "":
                listMultipleTextureTags.append(t)
        if  type(t) == c4d.TextureTag and t.GetMaterial() is None:
            t.Remove()
    increment = 0
    for tTags in  listMultipleTextureTags:
        print(increment)
        selection =  listMultipleTextureTags[increment][c4d.TEXTURETAG_RESTRICTION]
        print(selection)
        if len(listMultipleTextureTags) !=  (increment + 1):
           listMultipleTextureTags[increment].Remove()
        increment = increment + 1
    doc.SetActiveObject(obj)
    c4d.CallCommand(12236)      
   # c4d.CallCommand(100004787)
    c4d.documents.SetActiveDocument(doc)
    
def cleanObjects(x,objects):
    string = x.GetName()
    if string.find(".") != -1:
        string = string.replace(".", "")
    if objects.count(string) == 0:
        objects.append(string)
    else:
        string = findNameObject(string, objects,0)
        objects.append(string)
    x.SetName(string) 
    c4d.documents.SetActiveDocument(doc)


def main():
    cleanMaterials()
    objects = []
    for obj in doc.GetObjects():
        iterateChildren(obj, objects)
    
    

if __name__=='__main__':
    main()
