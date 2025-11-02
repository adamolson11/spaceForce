using UnityEngine;

/// <summary>
/// Attach to a sphere mesh representing a planet. Assign a Material with the planet albedo/normal maps.
/// Supports self-rotation (day), axial tilt and a simple circular orbit mode for visuals.
/// </summary>
[RequireComponent(typeof(Renderer))]
public class PlanetController : MonoBehaviour
{
    [Header("Visual")]
    public Material planetMaterial; // assign a material using planet texture(s)
    [Tooltip("Degrees per second for self rotation (planet day)")]
    public float rotationDegreesPerSecond = 10f;
    [Tooltip("Axial tilt in degrees (visual)")]
    public float axialTiltDegrees = 0f;

    [Header("Orbit (visual only)")]
    public bool useOrbit = false;
    public Transform orbitCenter;
    [Tooltip("Visual orbit radius in world units")]
    public float orbitRadius = 10f;
    [Tooltip("Time (seconds) to complete one orbit")]
    public float orbitPeriodSeconds = 60f;

    private float orbitAngle = 0f;

    void Start()
    {
        if (planetMaterial != null)
            GetComponent<Renderer>().material = planetMaterial;

        // Set axial tilt by rotating the mesh locally once
        transform.localRotation = Quaternion.Euler(axialTiltDegrees, 0f, 0f);
    }

    void Update()
    {
        // Self rotation
        transform.Rotate(Vector3.up, rotationDegreesPerSecond * Time.deltaTime, Space.Self);

        // Simple circular orbit in XZ plane (visual)
        if (useOrbit && orbitCenter != null && orbitPeriodSeconds > 0f)
        {
            orbitAngle += (360f / orbitPeriodSeconds) * Time.deltaTime;
            float rad = Mathf.Deg2Rad * orbitAngle;
            Vector3 pos = orbitCenter.position + new Vector3(Mathf.Cos(rad), 0f, Mathf.Sin(rad)) * orbitRadius;
            transform.position = pos;
        }
    }
}