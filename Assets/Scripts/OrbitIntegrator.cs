using UnityEngine;

/// <summary>
/// A simple gravitational integrator for orbiting around a central massive body.
/// Not using Unity collision physics for the orbit integration — this is a game-ready semi-implicit integrator.
/// Use scaled units for mu (G*M) that match your visual/physics scaling.
/// </summary>
public class OrbitIntegrator : MonoBehaviour
{
    public Transform centralBody;
    [Tooltip("Gravitational parameter mu = G * M (choose scaled units)")]
    public float gravitationalParameter = 398600.4418f; // choose a scaled value appropriate to your scene
    public Vector3 velocity;

    void FixedUpdate()
    {
        if (centralBody == null) return;
        Vector3 r = transform.position - centralBody.position;
        float dist = r.magnitude;
        if (dist <= Mathf.Epsilon) return;

        // acceleration toward central body
        Vector3 a = -gravitationalParameter * r / (dist * dist * dist);

        // semi-implicit Euler integration
        velocity += a * Time.fixedDeltaTime;
        transform.position += velocity * Time.fixedDeltaTime;
    }
}