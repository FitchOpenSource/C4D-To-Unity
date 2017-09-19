using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;


public class MaterialImportOptions : AssetPostprocessor
{
	
	  // Before Material is imported we modify default settings
	 

    Material OnAssignMaterialModel(Material mat, Renderer renderer)
    {
		
		 //Copy default Material
		  
		Material material = new Material(mat);
        bool Loaded = false;


		//Check if material directory exists if not create it 
		if (!Directory.Exists(Application.dataPath + "/Material"))
        {
            //if it doesn't, create it
            Directory.CreateDirectory(Application.dataPath + "/Material");

        }


		 //If material has no name, create a default one
        if (material.name == "")
			material.name = "defaultName";


		 //Material path	 
     	var materialPath = "Assets/Material/" + material.name + ".mat";


		//Load Material if it already exists		 
		if (AssetDatabase.LoadAssetAtPath(materialPath, typeof(Material)))
        {
            material = (Material)AssetDatabase.LoadAssetAtPath(materialPath, typeof(Material));
            Loaded = true;
        }


		bool hasAlpha = false;

		// This is the lab renderer shader for the Unity asset store, I use it for VR purpose
		material.shader = Shader.Find("Valve/vr_standard");
		// Use the default one if not using VR
		if (material.shader == null)
			material.shader = Shader.Find("Standard");

		//Remove default texture Unity has assigned (Can mess up things if you have an ALPHA and COLOR texture)
		material.mainTexture = null;

		//Remove default texture Unity has assigned
		material.SetTexture("_DetailAlbedoMap", null);

		//Check if Material has assigned Alpha texture to it and if it is inverted
		string[] matchingAssets = AssetDatabase.FindAssets(AbsoluteName(material.name) + "INVERTALPHA");

		//if not Check if Material has assigned Alpha texture
		if ((matchingAssets.Length == 0)) 
		{
			matchingAssets = AssetDatabase.FindAssets (AbsoluteName (material.name) + "ALPHA");
		}

		// If asset is found
		if (matchingAssets.Length > 0)
		{
			// Load Texture
			Texture currentTexture = AssetDatabase.LoadAssetAtPath(AssetDatabase.GUIDToAssetPath(matchingAssets[0]), typeof(Texture)) as Texture;
			if (currentTexture != null && material != null)
			{

				// Assign texture and set mode to ALphaBend or Fade
				material.SetFloat ("_Mode", 2);
				material.mainTexture = currentTexture;

				//Since there is already a texture set color to white
				material.color = new Color (1, 1, 1, material.color.a);
				hasAlpha = true;

			
			}
		}
	
	//Check if Material has assigned Color texture
     matchingAssets = AssetDatabase.FindAssets(AbsoluteName(material.name) + "COLOR");
	
		// If asset is found
     if (matchingAssets.Length > 0)
        {
		// Load Texture
          Texture currentTexture = AssetDatabase.LoadAssetAtPath(AssetDatabase.GUIDToAssetPath(matchingAssets[0]), typeof(Texture)) as Texture;
			if (currentTexture != null && material != null) 
			{
				// If material already has alpha,  set it to second albedo Map (this makes it look the same as in cinema)
				if (hasAlpha == true)
					material.SetTexture ("_DetailAlbedoMap", currentTexture);
				else 
				{
					// if no Alpha texture, set texture to main texture
					material.mainTexture = currentTexture;
					material.color = new Color (1, 1, 1, material.color.a);
				}
			}
        }

		//Check if Material has assigned Bump texture
        matchingAssets = AssetDatabase.FindAssets(AbsoluteName(material.name) + "BUMP");

		// If asset is found
		if (matchingAssets.Length > 0)
        {
			// Load Texture
            Texture currentTexture = AssetDatabase.LoadAssetAtPath(AssetDatabase.GUIDToAssetPath(matchingAssets[0]), typeof(Texture)) as Texture;
            if (currentTexture != null && material != null)
            {
				// set Bump texture to shader
				material.SetTexture("_BumpMap", currentTexture);
            }
        }

		//Check if Material has assigned LUMINANCE texture
		matchingAssets = AssetDatabase.FindAssets(AbsoluteName(material.name) + "LUMINANCE");

		// If asset is found
		if (matchingAssets.Length > 0)
		{
			// Load Texture
			Texture currentTexture = AssetDatabase.LoadAssetAtPath(AssetDatabase.GUIDToAssetPath(matchingAssets[0]), typeof(Texture)) as Texture;
			if (currentTexture != null && material != null) 
			{

				// Use default main material for better Color,  use White as default
				material.SetTexture("_EmissionMap", material.mainTexture);
				material.SetColor("_EmissionColor", Color.white);
			}
		}
	// If material doesn't exist, create it
     if (Loaded == false)
        AssetDatabase.CreateAsset(material, "Assets/Material/" + material.name + ".mat");
     return null;
    }

	// Get Initial Name with out "." (ex:Mat1.12 -> Mat1), Unity Converts texture tags as new materials
    private string AbsoluteName(string name)
    {
        name = name.Split('.')[0];
        //Debug.Log(name);
        return name;
    }

    void OnPostprocessModel(GameObject gameObject)
    {
        Process(gameObject.transform);
    }

	// Assign material once they have been created
    void Process(Transform gameObject)
    {
		// Replace default Material by Our own
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

		// If no material were assigned in c4d, add default material 
        if (gameObject.GetComponent<MeshRenderer>() != null  && gameObject.GetComponent<MeshRenderer>().sharedMaterial == null)
        {
            var materialPath = "Assets/Material/" + "Default" + ".mat";
            Material mat;
            if (!AssetDatabase.LoadAssetAtPath(materialPath, typeof(Material)))
            {
				if (Shader.Find("Valve/vr_standard"))
                	AssetDatabase.CreateAsset(new Material(Shader.Find("Valve/vr_standard")), materialPath);
				else
					AssetDatabase.CreateAsset(new Material(Shader.Find("Standard")), materialPath);
			}
            mat = (Material)AssetDatabase.LoadAssetAtPath(materialPath, typeof(Material));
            gameObject.GetComponent<MeshRenderer>().sharedMaterial = mat;
        }

        foreach (Transform t in gameObject)
            Process(t);
    }


	void OnPostprocessTexture(Texture2D texturea)
	{
		// Cinema Generates Alpha via Saturation

		//if texture has ALPHA and is Inverted
		if (assetPath.Contains("INVERTALPHA") == true) 
		{
			
			for (int m = 0; m < texturea.mipmapCount; m++) {
				Color[] c = texturea.GetPixels (m);

				for (int i = 0; i < c.Length; i++) {

					//Calculate saturation
					c [i] = CalculateSaturation (c[i]);

					// Invert Gray Scale
					c [i].a =  1 - c [i].grayscale;

				}
				texturea.SetPixels (c, m);
			}
		}
		//if texture has ALPHA 
		else if (assetPath.Contains("ALPHA") == true)
			
			for (int m = 0; m < texturea.mipmapCount; m++) 
			{
				Color[] c = texturea.GetPixels (m);

				for (int i = 0; i < c.Length; i++) 
				{
					//Calculate saturation
					c[i] = CalculateSaturation (c[i]);
					//Invert Gray Scale
					c [i].a = c [i].grayscale; 
				}
				texturea.SetPixels (c, m);
			}
		// Instead of setting pixels for each mip map levels, you can also
		// modify only the pixels in the highest mip level. And then simply use
		// texture.Apply(true); to generate lower mip levels.
	}

	void OnPreprocessTexture()
	{
		// Make Bump as Normal

		if (assetPath.Contains("BUMP"))
		{
			TextureImporter textureImporter  = (TextureImporter)assetImporter;
			textureImporter.textureType = TextureImporterType.NormalMap;
			textureImporter.convertToNormalmap = true;
			textureImporter.heightmapScale = 0.01f;

			textureImporter.alphaSource = TextureImporterAlphaSource.FromGrayScale;


		}
		// Set Alpha Texture Parameter
		if (assetPath.Contains ("ALPHA")) 
		{
			TextureImporter textureImporter = (TextureImporter)assetImporter;
			textureImporter.alphaSource = TextureImporterAlphaSource.FromGrayScale;
			textureImporter.sRGBTexture = false;
		}


	}

	//https://www.niwa.nu/2013/05/math-behind-colorspace-conversions-rgb-hsl/
	public Color CalculateSaturation(Color pixel)
	{
		float R = pixel.r;
		float G = pixel.g;
		float B = pixel.b;

		float finalR;
		float finalG;
		float finalB;

		float min;
		float max;

		float luminance;
		float saturation;
		float HUE = 1;

		max = Mathf.Max (R, G);
		max = Mathf.Max (max, B);

		min = Mathf.Min (R, G);
		min = Mathf.Max (min, B);

		luminance = (min + max) / 2;
		if (min == max) 
		{
			saturation = 0;

		}
		else if (luminance < 0.5f) 
		{
			saturation = (max - min) / (max + min);
		}
		else
			saturation = (max - min) / (2.0f - max - min);
		saturation = 0;
		if (R > G && R > B) {
			HUE = (G - B) / (max - min);
		} else if (G > R && G > B) {
			HUE = 2.0f + (B - R) / (max - min);
		} else if (B > R && B > G) {
			HUE = 4.0f + (R - G) / (max - min);
		}
		HUE = HUE * 60f;
		if (HUE < 0)
			HUE += 360; 
		
		float temporary_1;
		if (luminance < 0.5f) 
		{
			temporary_1 = luminance * (1.0f + saturation);
		}
		else
		{
			temporary_1 =  luminance + saturation - luminance * saturation;
		}
		float temporary_2;
		temporary_2 = 2 * luminance - temporary_1;
		HUE = HUE/360f;
		float temporary_R = HUE + 0.333f;
		float temporary_G = HUE;
		float temporary_B = HUE - 0.333f;

		if (temporary_R < 0)
			temporary_R += 1;
		if (temporary_R > 1)
			temporary_R += -1;
		
		if (temporary_G < 0)
			temporary_G += 1;
		if (temporary_G > 1)
			temporary_G += -1;
		
		if (temporary_B < 0)
			temporary_B += 1;
		if (temporary_B > 1)
			temporary_B += -1;

		if (temporary_R * 6 < 1)
			finalR = temporary_2 + (temporary_1 - temporary_2) * 6 * temporary_R;
		else if (temporary_R * 2 < 1)
			finalR = temporary_1;
		else if (3*temporary_R  < 2)
			finalR =  temporary_2 + (temporary_1 - temporary_2) * (0.666f - temporary_R) * 6;
		else
			finalR = temporary_2;

		if (temporary_G * 6 < 1)
			finalG = temporary_2 + (temporary_1 - temporary_2) * 6 * temporary_G;
		else if (temporary_G * 2 < 1)
			finalG = temporary_1;
		else if (3*temporary_G  < 2)
			finalG =  temporary_2 + (temporary_1 - temporary_2) * (0.666f - temporary_G) * 6;
		else
			finalG = temporary_2;
		
		if (temporary_B * 6 < 1)
			finalB = temporary_2 + (temporary_1 - temporary_2) * 6 * temporary_B;
		else if (temporary_B * 2 < 1)
			finalB = temporary_1;
		else if (3*temporary_B  < 2)
			finalB =  temporary_2 + (temporary_1 - temporary_2) * (0.666f - temporary_B) * 6;
		else
			finalB = temporary_2;

		return (new Color(finalR,finalG,finalB));
		

	}

}

