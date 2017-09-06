using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;

public class MaterialImportOptions : AssetPostprocessor
{

    Material OnAssignMaterialModel(Material mat, Renderer renderer)
    {
        Material material = new Material(mat);
        bool Loaded = false;
        if (!Directory.Exists(Application.dataPath + "/Material"))
        {
            //if it doesn't, create it
            Directory.CreateDirectory(Application.dataPath + "/Material");

        }
        if (material.name == "")
            material.name = "toto";
     var materialPath = "Assets/Material/" + material.name + ".mat";
     material = (Material)AssetDatabase.LoadAssetAtPath(materialPath, typeof(Material));
     Loaded = true;



     material.shader = Shader.Find("Valve/vr_standard");

     material.SetInt("g_bRenderBackfaces", 1);
        // Assign Baked Texture to Material
        string[] matchingAssets = AssetDatabase.FindAssets(AbsoluteName(material.name) + "COLOR");
     if (matchingAssets.Length > 0)
        {
          Texture currentTexture = AssetDatabase.LoadAssetAtPath(AssetDatabase.GUIDToAssetPath(matchingAssets[0]), typeof(Texture)) as Texture;
           if (currentTexture != null && material != null)
              material.mainTexture = currentTexture;
        }

        matchingAssets = AssetDatabase.FindAssets(AbsoluteName(material.name) + "BUMP");
        if (matchingAssets.Length > 0)
        {
            Texture currentTexture = AssetDatabase.LoadAssetAtPath(AssetDatabase.GUIDToAssetPath(matchingAssets[0]), typeof(Texture)) as Texture;
            if (currentTexture != null && material != null)
            {
                material.SetTexture("_BumpMap", currentTexture);
            }
        }

        matchingAssets = AssetDatabase.FindAssets(AbsoluteName(material.name) + "ALPHA");
        if (matchingAssets.Length > 0)
        {
            Texture currentTexture = AssetDatabase.LoadAssetAtPath(AssetDatabase.GUIDToAssetPath(matchingAssets[0]), typeof(Texture)) as Texture;
            if (currentTexture != null && material != null)
            {
                material.mainTexture = currentTexture;
            }
        }
     if (Loaded == false)
        AssetDatabase.CreateAsset(material, "Assets/Material/" + material.name + ".mat");
     return null;
    }

    private string AbsoluteName(string name)
    {
        name = name.Split('.')[0];
        Debug.Log(name);
        return name;
    }

    void OnPostprocessModel(GameObject gameObject)
    {
        Process(gameObject.transform);
    }
    void Process(Transform gameObject)
    {
        if (gameObject.GetComponent<MeshRenderer>() != null && gameObject.GetComponent<MeshRenderer>().sharedMaterial != null)
        {
            Material[] mats = new Material[gameObject.GetComponent<MeshRenderer>().sharedMaterials.Length];
            for (int increment = 0; increment < gameObject.GetComponent<MeshRenderer>().sharedMaterials.Length; increment++)
            {
                if (gameObject.GetComponent<MeshRenderer>().sharedMaterials[increment] != null)
                {
                    string materialPath = "Assets/Material/" + gameObject.GetComponent<MeshRenderer>().sharedMaterials[increment].name + ".mat";
                    mats[increment] = (Material)AssetDatabase.LoadAssetAtPath(materialPath, typeof(Material));

                    Debug.Log("here");
                }
            }
            gameObject.GetComponent<MeshRenderer>().sharedMaterials = mats;
        }
        if (gameObject.GetComponent<MeshRenderer>() != null  && gameObject.GetComponent<MeshRenderer>().sharedMaterial == null)
        {
            var materialPath = "Assets/Material/" + "Default" + ".mat";
            Material mat;
            if (!AssetDatabase.LoadAssetAtPath(materialPath, typeof(Material)))
            {
                AssetDatabase.CreateAsset(new Material(Shader.Find("Valve/vr_standard")), materialPath);
            }
            mat = (Material)AssetDatabase.LoadAssetAtPath(materialPath, typeof(Material));
            gameObject.GetComponent<MeshRenderer>().sharedMaterial = mat;
        }

        foreach (Transform t in gameObject)
            Process(t);
    }

}

