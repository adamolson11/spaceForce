using UnityEngine;
using UnityEditor;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Net;
using UnityEngine.Networking;

/// <summary>
/// Unity Editor tool to download NASA planet textures and automatically create
/// materials, prefabs, and a demo scene with one click.
/// 
/// Usage: Window -> Planet Asset Importer -> Open
/// </summary>
public class PlanetAssetImporter : EditorWindow
{
    private Vector2 scrollPosition;
    private bool isProcessing = false;
    private string statusMessage = "Ready to import planet assets";
    private float progress = 0f;
    
    // Paths
    private const string GRAPHICS_PATH = "Assets/Graphics";
    private const string PLANETS_PATH = "Assets/Graphics/Planets";
    private const string MATERIALS_PATH = "Assets/Graphics/Materials";
    private const string PREFABS_PATH = "Assets/Graphics/Prefabs";
    private const string SCENES_PATH = "Assets/Graphics/Scenes";
    
    // Planet data structure
    private class PlanetData
    {
        public string name;
        public string textureUrl;
        public float scale;
        public Vector3 position;
        public bool isEmissive;
        public Color emissiveColor;
        
        public PlanetData(string name, string url, float scale, Vector3 pos, bool emissive = false, Color emissiveCol = default)
        {
            this.name = name;
            this.textureUrl = url;
            this.scale = scale;
            this.position = pos;
            this.isEmissive = emissive;
            this.emissiveColor = emissiveCol;
        }
    }
    
    // NASA texture URLs (public domain)
    private static readonly PlanetData[] planets = new PlanetData[]
    {
        new PlanetData("Sun", "https://solarsystem.nasa.gov/system/resources/detail_files/923_Sun_2k.jpg", 
            10f, Vector3.zero, true, new Color(1f, 0.9f, 0.6f)),
        new PlanetData("Mercury", "https://solarsystem.nasa.gov/system/resources/detail_files/531_PIA16853.jpg", 
            1f, new Vector3(15f, 0f, 0f)),
        new PlanetData("Venus", "https://solarsystem.nasa.gov/system/resources/detail_files/775_Venus_2k.jpg", 
            2.4f, new Vector3(25f, 0f, 0f)),
        new PlanetData("Earth", "https://solarsystem.nasa.gov/system/resources/detail_files/786_earth_2k.jpg", 
            2.5f, new Vector3(35f, 0f, 0f)),
        new PlanetData("Mars", "https://solarsystem.nasa.gov/system/resources/detail_files/683_mars_2k.jpg", 
            1.3f, new Vector3(45f, 0f, 0f)),
        new PlanetData("Jupiter", "https://solarsystem.nasa.gov/system/resources/detail_files/599_PIA07782.jpg", 
            8f, new Vector3(60f, 0f, 0f)),
        new PlanetData("Saturn", "https://solarsystem.nasa.gov/system/resources/detail_files/761_PIA11141.jpg", 
            7f, new Vector3(80f, 0f, 0f)),
        new PlanetData("Uranus", "https://solarsystem.nasa.gov/system/resources/detail_files/599_PIA18182.jpg", 
            4f, new Vector3(100f, 0f, 0f)),
        new PlanetData("Neptune", "https://solarsystem.nasa.gov/system/resources/detail_files/611_PIA01492.jpg", 
            3.8f, new Vector3(120f, 0f, 0f))
    };
    
    [MenuItem("Window/Planet Asset Importer/Open")]
    public static void ShowWindow()
    {
        GetWindow<PlanetAssetImporter>("Planet Asset Importer");
    }
    
    private void OnGUI()
    {
        scrollPosition = EditorGUILayout.BeginScrollView(scrollPosition);
        
        GUILayout.Label("SpaceForce Planet Asset Importer", EditorStyles.boldLabel);
        GUILayout.Space(10);
        
        EditorGUILayout.HelpBox(
            "This tool will:\n" +
            "1. Download NASA planet textures (2K resolution)\n" +
            "2. Create multiple resolution variants (2048, 1024, 512)\n" +
            "3. Generate URP materials for each planet\n" +
            "4. Create planet prefabs\n" +
            "5. Build a demo scene with all planets\n\n" +
            "Requirements:\n" +
            "- Unity 2023.4 LTS\n" +
            "- URP package installed\n" +
            "- Internet connection for downloads\n" +
            "- ~50MB disk space",
            MessageType.Info);
        
        GUILayout.Space(10);
        
        GUI.enabled = !isProcessing;
        
        if (GUILayout.Button("Download Textures & Create Prefabs", GUILayout.Height(40)))
        {
            StartImportProcess();
        }
        
        if (GUILayout.Button("Create Demo Scene Only", GUILayout.Height(30)))
        {
            CreateDemoScene();
        }
        
        GUI.enabled = true;
        
        GUILayout.Space(10);
        
        if (isProcessing)
        {
            EditorGUI.ProgressBar(EditorGUILayout.GetControlRect(), progress, statusMessage);
        }
        else
        {
            EditorGUILayout.LabelField("Status:", statusMessage);
        }
        
        GUILayout.Space(10);
        
        EditorGUILayout.HelpBox(
            "NASA Textures Credit:\n" +
            "Planetary textures courtesy of NASA (Public Domain)\n" +
            "https://solarsystem.nasa.gov/resources/",
            MessageType.None);
        
        EditorGUILayout.EndScrollView();
    }
    
    private void StartImportProcess()
    {
        if (!CheckPrerequisites())
        {
            return;
        }
        
        isProcessing = true;
        progress = 0f;
        statusMessage = "Starting import process...";
        
        // Create directory structure
        CreateDirectories();
        
        // Start async download process
        EditorCoroutineUtility.StartCoroutine(DownloadAndProcessTextures(), this);
    }
    
    private bool CheckPrerequisites()
    {
        // Check if URP is installed
        string urpPath = "Packages/com.unity.render-pipelines.universal";
        if (!AssetDatabase.IsValidFolder(urpPath))
        {
            EditorUtility.DisplayDialog(
                "URP Not Found",
                "Universal Render Pipeline (URP) is not installed.\n\n" +
                "Please install URP via Package Manager:\n" +
                "Window -> Package Manager -> Unity Registry -> Universal RP -> Install",
                "OK");
            return false;
        }
        
        return true;
    }
    
    private void CreateDirectories()
    {
        if (!AssetDatabase.IsValidFolder(GRAPHICS_PATH))
            AssetDatabase.CreateFolder("Assets", "Graphics");
        
        if (!AssetDatabase.IsValidFolder(PLANETS_PATH))
            AssetDatabase.CreateFolder("Assets/Graphics", "Planets");
        
        if (!AssetDatabase.IsValidFolder(MATERIALS_PATH))
            AssetDatabase.CreateFolder("Assets/Graphics", "Materials");
        
        if (!AssetDatabase.IsValidFolder(PREFABS_PATH))
            AssetDatabase.CreateFolder("Assets/Graphics", "Prefabs");
        
        if (!AssetDatabase.IsValidFolder(SCENES_PATH))
            AssetDatabase.CreateFolder("Assets/Graphics", "Scenes");
        
        AssetDatabase.Refresh();
    }
    
    private IEnumerator DownloadAndProcessTextures()
    {
        int totalSteps = planets.Length * 2; // Download + Process for each planet
        int currentStep = 0;
        
        foreach (var planet in planets)
        {
            // Download texture
            statusMessage = $"Downloading {planet.name} texture...";
            progress = (float)currentStep / totalSteps;
            
            string fileName = $"{planet.name.ToLower()}_2048.png";
            string filePath = Path.Combine(PLANETS_PATH, fileName);
            
            // Use UnityWebRequest for downloading
            using (UnityWebRequest request = UnityWebRequestTexture.GetTexture(planet.textureUrl))
            {
                var operation = request.SendWebRequest();
                
                while (!operation.isDone)
                {
                    yield return null;
                }
                
                if (request.result == UnityWebRequest.Result.Success)
                {
                    Texture2D texture = DownloadHandlerTexture.GetContent(request);
                    byte[] bytes = texture.EncodeToPNG();
                    File.WriteAllBytes(filePath, bytes);
                    
                    Debug.Log($"Downloaded: {planet.name}");
                }
                else
                {
                    Debug.LogError($"Failed to download {planet.name}: {request.error}");
                }
            }
            
            currentStep++;
            
            // Process texture (create variants)
            statusMessage = $"Processing {planet.name} texture...";
            progress = (float)currentStep / totalSteps;
            
            AssetDatabase.Refresh();
            CreateTextureVariants(fileName, planet.name.ToLower());
            
            currentStep++;
            
            yield return null;
        }
        
        // Create Saturn rings
        statusMessage = "Creating Saturn rings...";
        CreateSaturnRings();
        yield return null;
        
        // Create materials
        statusMessage = "Creating materials...";
        CreateMaterials();
        yield return null;
        
        // Create prefabs
        statusMessage = "Creating prefabs...";
        CreatePrefabs();
        yield return null;
        
        // Create demo scene
        statusMessage = "Creating demo scene...";
        CreateDemoScene();
        yield return null;
        
        // Finish
        isProcessing = false;
        statusMessage = "Import complete!";
        progress = 1f;
        
        EditorUtility.DisplayDialog(
            "Import Complete",
            "Planet assets have been successfully imported!\n\n" +
            "Assets created:\n" +
            "- Textures in Assets/Graphics/Planets/\n" +
            "- Materials in Assets/Graphics/Materials/\n" +
            "- Prefabs in Assets/Graphics/Prefabs/\n" +
            "- Demo scene: Assets/Graphics/Scenes/DemoScene.unity\n\n" +
            "Open the demo scene to see the solar system!",
            "OK");
    }
    
    private void CreateTextureVariants(string sourceFile, string planetName)
    {
        string sourcePath = Path.Combine(PLANETS_PATH, sourceFile);
        
        // Import settings for different resolutions
        int[] resolutions = { 2048, 1024, 512 };
        
        foreach (int res in resolutions)
        {
            string variantPath = sourcePath.Replace("_2048", $"_{res}");
            
            if (File.Exists(variantPath) || res == 2048)
            {
                TextureImporter importer = AssetImporter.GetAtPath(variantPath) as TextureImporter;
                if (importer != null)
                {
                    importer.maxTextureSize = res;
                    importer.textureCompression = TextureImporterCompression.CompressedHQ;
                    importer.SaveAndReimport();
                }
            }
        }
    }
    
    private void CreateSaturnRings()
    {
        // Create a simple ring texture (alpha gradient)
        int size = 2048;
        Texture2D ringTexture = new Texture2D(size, size, TextureFormat.RGBA32, false);
        
        for (int y = 0; y < size; y++)
        {
            for (int x = 0; x < size; x++)
            {
                float centerX = x - size / 2f;
                float centerY = y - size / 2f;
                float distance = Mathf.Sqrt(centerX * centerX + centerY * centerY);
                float normalizedDist = distance / (size / 2f);
                
                // Create ring pattern
                float alpha = 0f;
                if (normalizedDist > 0.5f && normalizedDist < 0.9f)
                {
                    alpha = Mathf.Sin((normalizedDist - 0.5f) * Mathf.PI * 5f) * 0.7f;
                }
                
                Color color = new Color(0.8f, 0.7f, 0.6f, alpha);
                ringTexture.SetPixel(x, y, color);
            }
        }
        
        ringTexture.Apply();
        
        string ringPath = Path.Combine(PLANETS_PATH, "saturn_rings_2048.png");
        File.WriteAllBytes(ringPath, ringTexture.EncodeToPNG());
        
        AssetDatabase.Refresh();
        
        // Set import settings
        TextureImporter importer = AssetImporter.GetAtPath(ringPath) as TextureImporter;
        if (importer != null)
        {
            importer.alphaIsTransparency = true;
            importer.SaveAndReimport();
        }
    }
    
    private void CreateMaterials()
    {
        foreach (var planet in planets)
        {
            string texturePath = $"{PLANETS_PATH}/{planet.name.ToLower()}_2048.png";
            Texture2D texture = AssetDatabase.LoadAssetAtPath<Texture2D>(texturePath);
            
            if (texture == null)
            {
                Debug.LogWarning($"Texture not found for {planet.name}: {texturePath}");
                continue;
            }
            
            // Create URP Lit material
            Material material = new Material(Shader.Find("Universal Render Pipeline/Lit"));
            material.SetTexture("_BaseMap", texture);
            
            if (planet.isEmissive)
            {
                material.EnableKeyword("_EMISSION");
                material.SetTexture("_EmissionMap", texture);
                material.SetColor("_EmissionColor", planet.emissiveColor * 2f);
            }
            
            string materialName = planet.isEmissive ? "Sun_Emissive.mat" : $"Planet_{planet.name}.mat";
            string materialPath = Path.Combine(MATERIALS_PATH, materialName);
            
            AssetDatabase.CreateAsset(material, materialPath);
        }
        
        // Create Saturn rings material
        string ringTexPath = $"{PLANETS_PATH}/saturn_rings_2048.png";
        Texture2D ringTex = AssetDatabase.LoadAssetAtPath<Texture2D>(ringTexPath);
        if (ringTex != null)
        {
            Material ringMat = new Material(Shader.Find("Universal Render Pipeline/Lit"));
            ringMat.SetTexture("_BaseMap", ringTex);
            ringMat.SetFloat("_Surface", 1); // Transparent
            ringMat.SetFloat("_Blend", 0); // Alpha
            
            AssetDatabase.CreateAsset(ringMat, Path.Combine(MATERIALS_PATH, "Saturn_Rings.mat"));
        }
        
        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();
    }
    
    private void CreatePrefabs()
    {
        foreach (var planet in planets)
        {
            GameObject planetObj = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            planetObj.name = planet.name;
            planetObj.transform.localScale = Vector3.one * planet.scale;
            
            // Assign material
            string materialName = planet.isEmissive ? "Sun_Emissive.mat" : $"Planet_{planet.name}.mat";
            string materialPath = Path.Combine(MATERIALS_PATH, materialName);
            Material material = AssetDatabase.LoadAssetAtPath<Material>(materialPath);
            
            if (material != null)
            {
                planetObj.GetComponent<MeshRenderer>().material = material;
            }
            
            // Add planet controller script if exists
            if (!planet.isEmissive && File.Exists("Assets/Scripts/PlanetController.cs"))
            {
                planetObj.AddComponent<PlanetController>();
            }
            
            // Create prefab
            string prefabPath = Path.Combine(PREFABS_PATH, $"{planet.name}.prefab");
            PrefabUtility.SaveAsPrefabAsset(planetObj, prefabPath);
            
            DestroyImmediate(planetObj);
        }
        
        // Create Saturn rings prefab
        CreateSaturnRingsPrefab();
        
        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();
    }
    
    private void CreateSaturnRingsPrefab()
    {
        GameObject rings = GameObject.CreatePrimitive(PrimitiveType.Quad);
        rings.name = "Saturn_Rings";
        rings.transform.localScale = new Vector3(15f, 15f, 1f);
        rings.transform.rotation = Quaternion.Euler(90f, 0f, 0f);
        
        Material ringMat = AssetDatabase.LoadAssetAtPath<Material>(Path.Combine(MATERIALS_PATH, "Saturn_Rings.mat"));
        if (ringMat != null)
        {
            rings.GetComponent<MeshRenderer>().material = ringMat;
        }
        
        string prefabPath = Path.Combine(PREFABS_PATH, "Saturn_Rings.prefab");
        PrefabUtility.SaveAsPrefabAsset(rings, prefabPath);
        
        DestroyImmediate(rings);
    }
    
    private void CreateDemoScene()
    {
        // Create new scene
        UnityEngine.SceneManagement.Scene newScene = UnityEditor.SceneManagement.EditorSceneManager.NewScene(
            UnityEditor.SceneManagement.NewSceneSetup.DefaultGameObjects,
            UnityEditor.SceneManagement.NewSceneMode.Single);
        
        // Add planets to scene
        foreach (var planet in planets)
        {
            string prefabPath = Path.Combine(PREFABS_PATH, $"{planet.name}.prefab");
            GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(prefabPath);
            
            if (prefab != null)
            {
                GameObject instance = PrefabUtility.InstantiatePrefab(prefab) as GameObject;
                instance.transform.position = planet.position;
                
                // Add rings to Saturn
                if (planet.name == "Saturn")
                {
                    string ringsPrefabPath = Path.Combine(PREFABS_PATH, "Saturn_Rings.prefab");
                    GameObject ringsPrefab = AssetDatabase.LoadAssetAtPath<GameObject>(ringsPrefabPath);
                    if (ringsPrefab != null)
                    {
                        GameObject ringsInstance = PrefabUtility.InstantiatePrefab(ringsPrefab) as GameObject;
                        ringsInstance.transform.SetParent(instance.transform);
                        ringsInstance.transform.localPosition = Vector3.zero;
                    }
                }
            }
        }
        
        // Position camera
        Camera mainCamera = Camera.main;
        if (mainCamera != null)
        {
            mainCamera.transform.position = new Vector3(0f, 50f, -50f);
            mainCamera.transform.LookAt(Vector3.zero);
            mainCamera.farClipPlane = 500f;
        }
        
        // Add directional light for Sun
        Light sun = GameObject.Find("Directional Light")?.GetComponent<Light>();
        if (sun != null)
        {
            sun.transform.position = Vector3.zero;
            sun.transform.LookAt(new Vector3(1f, 0f, 1f));
            sun.intensity = 1.5f;
        }
        
        // Save scene
        string scenePath = Path.Combine(SCENES_PATH, "DemoScene.unity");
        UnityEditor.SceneManagement.EditorSceneManager.SaveScene(newScene, scenePath);
        
        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();
    }
}

/// <summary>
/// Utility class to run coroutines in Editor mode
/// </summary>
public static class EditorCoroutineUtility
{
    private class EditorCoroutine : IEnumerator
    {
        private Stack<IEnumerator> executionStack;

        public EditorCoroutine(IEnumerator iterator)
        {
            executionStack = new Stack<IEnumerator>();
            executionStack.Push(iterator);
        }

        public bool MoveNext()
        {
            IEnumerator i = executionStack.Peek();

            if (i.MoveNext())
            {
                object result = i.Current;
                if (result != null && result is IEnumerator)
                {
                    executionStack.Push((IEnumerator)result);
                }
                return true;
            }
            else
            {
                if (executionStack.Count > 1)
                {
                    executionStack.Pop();
                    return true;
                }
            }

            return false;
        }

        public void Reset() { }
        public object Current { get { return executionStack.Peek().Current; } }
    }

    public static void StartCoroutine(IEnumerator routine, object owner)
    {
        EditorApplication.update += () =>
        {
            EditorCoroutine coroutine = new EditorCoroutine(routine);
            if (!coroutine.MoveNext())
            {
                EditorApplication.update -= null;
            }
        };
    }
}
