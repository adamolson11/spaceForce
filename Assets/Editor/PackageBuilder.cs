using UnityEngine;
using UnityEditor;
using System.IO;

/// <summary>
/// Unity Editor tool to export planet assets as a Unity package for distribution.
/// Creates a .unitypackage file containing all planet textures, materials, prefabs, and scenes.
/// 
/// Usage: Window -> Package Builder -> Open
/// </summary>
public class PackageBuilder : EditorWindow
{
    private Vector2 scrollPosition;
    private string packageName = "spaceforce_planet_assets";
    private string outputFolder = "Packages";
    private bool includeTextures = true;
    private bool includeMaterials = true;
    private bool includePrefabs = true;
    private bool includeScenes = true;
    private bool includeScripts = true;
    private string statusMessage = "Ready to build package";
    
    [MenuItem("Window/Package Builder/Open")]
    public static void ShowWindow()
    {
        GetWindow<PackageBuilder>("Package Builder");
    }
    
    private void OnGUI()
    {
        scrollPosition = EditorGUILayout.BeginScrollView(scrollPosition);
        
        GUILayout.Label("SpaceForce Package Builder", EditorStyles.boldLabel);
        GUILayout.Space(10);
        
        EditorGUILayout.HelpBox(
            "Build a Unity package (.unitypackage) containing planet assets.\n" +
            "Others can import this package to get all textures, materials, and prefabs.",
            MessageType.Info);
        
        GUILayout.Space(10);
        
        // Package settings
        GUILayout.Label("Package Settings", EditorStyles.boldLabel);
        packageName = EditorGUILayout.TextField("Package Name", packageName);
        outputFolder = EditorGUILayout.TextField("Output Folder", outputFolder);
        
        GUILayout.Space(10);
        
        // Include options
        GUILayout.Label("Include in Package", EditorStyles.boldLabel);
        includeTextures = EditorGUILayout.Toggle("Textures (Graphics/Planets/)", includeTextures);
        includeMaterials = EditorGUILayout.Toggle("Materials (Graphics/Materials/)", includeMaterials);
        includePrefabs = EditorGUILayout.Toggle("Prefabs (Graphics/Prefabs/)", includePrefabs);
        includeScenes = EditorGUILayout.Toggle("Scenes (Graphics/Scenes/)", includeScenes);
        includeScripts = EditorGUILayout.Toggle("Scripts (Scripts/)", includeScripts);
        
        GUILayout.Space(10);
        
        // Build buttons
        if (GUILayout.Button("Build Planet Assets Package", GUILayout.Height(40)))
        {
            BuildPackage();
        }
        
        if (GUILayout.Button("Build Complete Package (All Assets)", GUILayout.Height(30)))
        {
            BuildCompletePackage();
        }
        
        GUILayout.Space(10);
        
        EditorGUILayout.LabelField("Status:", statusMessage);
        
        GUILayout.Space(10);
        
        EditorGUILayout.HelpBox(
            "Package Contents:\n" +
            "- Planet textures (multiple resolutions)\n" +
            "- URP materials for each planet\n" +
            "- Planet prefabs ready to use\n" +
            "- Demo scene with solar system layout\n" +
            "- (Optional) C# scripts for planet control\n\n" +
            "Package will be saved to: " + GetOutputPath(),
            MessageType.None);
        
        EditorGUILayout.EndScrollView();
    }
    
    private string GetOutputPath()
    {
        return Path.Combine(outputFolder, $"{packageName}.unitypackage");
    }
    
    private void BuildPackage()
    {
        // Ensure output directory exists
        if (!Directory.Exists(outputFolder))
        {
            Directory.CreateDirectory(outputFolder);
        }
        
        // Collect asset paths
        System.Collections.Generic.List<string> assetPaths = new System.Collections.Generic.List<string>();
        
        if (includeTextures && AssetDatabase.IsValidFolder("Assets/Graphics/Planets"))
        {
            AddFolderAssets("Assets/Graphics/Planets", assetPaths);
        }
        
        if (includeMaterials && AssetDatabase.IsValidFolder("Assets/Graphics/Materials"))
        {
            AddFolderAssets("Assets/Graphics/Materials", assetPaths);
        }
        
        if (includePrefabs && AssetDatabase.IsValidFolder("Assets/Graphics/Prefabs"))
        {
            AddFolderAssets("Assets/Graphics/Prefabs", assetPaths);
        }
        
        if (includeScenes && AssetDatabase.IsValidFolder("Assets/Graphics/Scenes"))
        {
            AddFolderAssets("Assets/Graphics/Scenes", assetPaths);
        }
        
        if (includeScripts && AssetDatabase.IsValidFolder("Assets/Scripts"))
        {
            // Add specific scripts related to planets
            string[] scriptFiles = {
                "Assets/Scripts/PlanetController.cs",
                "Assets/Scripts/OrbitIntegrator.cs",
                "Assets/Scripts/ShipController.cs",
                "Assets/Scripts/ObjectPool.cs",
                "Assets/Scripts/Projectile.cs"
            };
            
            foreach (string script in scriptFiles)
            {
                if (File.Exists(script))
                {
                    assetPaths.Add(script);
                }
            }
        }
        
        if (assetPaths.Count == 0)
        {
            EditorUtility.DisplayDialog(
                "No Assets Found",
                "No assets found to package. Make sure you've created planet assets first.\n\n" +
                "Run: Window -> Planet Asset Importer -> Download Textures & Create Prefabs",
                "OK");
            statusMessage = "Error: No assets found";
            return;
        }
        
        // Export package
        string outputPath = GetOutputPath();
        
        try
        {
            AssetDatabase.ExportPackage(
                assetPaths.ToArray(),
                outputPath,
                ExportPackageOptions.Interactive | ExportPackageOptions.Recurse);
            
            statusMessage = $"Package built successfully: {outputPath}";
            
            EditorUtility.DisplayDialog(
                "Package Built",
                $"Package created successfully!\n\n" +
                $"Location: {outputPath}\n" +
                $"Assets included: {assetPaths.Count}\n\n" +
                $"To share:\n" +
                $"1. Send the .unitypackage file to team members\n" +
                $"2. They can import via: Assets -> Import Package -> Custom Package",
                "OK");
            
            // Reveal in explorer
            EditorUtility.RevealInFinder(outputPath);
        }
        catch (System.Exception e)
        {
            statusMessage = $"Error: {e.Message}";
            EditorUtility.DisplayDialog("Error", $"Failed to build package:\n{e.Message}", "OK");
        }
    }
    
    private void BuildCompletePackage()
    {
        // Temporarily set all options to true
        bool prevTextures = includeTextures;
        bool prevMaterials = includeMaterials;
        bool prevPrefabs = includePrefabs;
        bool prevScenes = includeScenes;
        bool prevScripts = includeScripts;
        
        includeTextures = true;
        includeMaterials = true;
        includePrefabs = true;
        includeScenes = true;
        includeScripts = true;
        
        packageName = "spaceforce_planet_assets_complete";
        BuildPackage();
        
        // Restore previous settings
        includeTextures = prevTextures;
        includeMaterials = prevMaterials;
        includePrefabs = prevPrefabs;
        includeScenes = prevScenes;
        includeScripts = prevScripts;
        packageName = "PlanetAssets";
    }
    
    private void AddFolderAssets(string folderPath, System.Collections.Generic.List<string> assetPaths)
    {
        string[] guids = AssetDatabase.FindAssets("", new[] { folderPath });
        
        foreach (string guid in guids)
        {
            string assetPath = AssetDatabase.GUIDToAssetPath(guid);
            if (!string.IsNullOrEmpty(assetPath) && !assetPaths.Contains(assetPath))
            {
                assetPaths.Add(assetPath);
            }
        }
    }
}

/// <summary>
/// Menu items for quick package building
/// </summary>
public static class QuickPackageBuilder
{
    [MenuItem("Tools/SpaceForce/Build Planet Package (Quick)")]
    public static void BuildQuickPackage()
    {
        string[] assetPaths = {
            "Assets/Graphics/Planets",
            "Assets/Graphics/Materials",
            "Assets/Graphics/Prefabs",
            "Assets/Graphics/Scenes"
        };
        
        // Filter to existing paths
        System.Collections.Generic.List<string> validPaths = new System.Collections.Generic.List<string>();
        foreach (string path in assetPaths)
        {
            if (AssetDatabase.IsValidFolder(path))
            {
                validPaths.Add(path);
            }
        }
        
        if (validPaths.Count == 0)
        {
            EditorUtility.DisplayDialog(
                "No Assets",
                "No planet assets found. Please create them first using:\n" +
                "Window -> Planet Asset Importer",
                "OK");
            return;
        }
        
        string outputPath = "Packages/spaceforce_planet_assets.unitypackage";
        
        // Ensure Packages folder exists
        if (!Directory.Exists("Packages"))
        {
            Directory.CreateDirectory("Packages");
        }
        
        try
        {
            AssetDatabase.ExportPackage(
                validPaths.ToArray(),
                outputPath,
                ExportPackageOptions.Recurse);
            
            Debug.Log($"Package built: {outputPath}");
            EditorUtility.RevealInFinder(outputPath);
            
            EditorUtility.DisplayDialog(
                "Success",
                $"Package created:\n{outputPath}",
                "OK");
        }
        catch (System.Exception e)
        {
            Debug.LogError($"Failed to build package: {e.Message}");
        }
    }
    
    [MenuItem("Tools/SpaceForce/Open Builds Folder")]
    public static void OpenBuildsFolder()
    {
        string buildsPath = Path.Combine(Application.dataPath, "..", "Builds");
        
        if (!Directory.Exists(buildsPath))
        {
            Directory.CreateDirectory(buildsPath);
        }
        
        EditorUtility.RevealInFinder(buildsPath);
    }
    
    [MenuItem("Tools/SpaceForce/About SpaceForce")]
    public static void AboutSpaceForce()
    {
        EditorUtility.DisplayDialog(
            "SpaceForce - Educational Game Project",
            "SpaceForce is an educational game platform teaching kids OOP and coding concepts " +
            "through space-themed games.\n\n" +
            "Features:\n" +
            "• Browser-based games (HTML/JS/Three.js)\n" +
            "• Unity 3D prototypes (C#)\n" +
            "• NASA planet textures (public domain)\n" +
            "• Educational quiz system\n\n" +
            "Repository: github.com/adamolson11/spaceForce\n" +
            "License: See LICENSE file",
            "OK");
    }
}
