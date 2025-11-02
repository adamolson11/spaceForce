using UnityEngine;

/// <summary>
/// Simple projectile behaviour. Use collider + trigger / physics layers to control collisions.
/// Projectile moves forward in its local forward direction (or uses its Rigidbody if present).
/// </summary>
[RequireComponent(typeof(Collider))]
public class Projectile : MonoBehaviour
{
    public float lifetime = 6f;
    public float speed = 80f;
    public bool useRigidbody = false;

    void Start()
    {
        Destroy(gameObject, lifetime);
    }

    void Update()
    {
        if (!useRigidbody)
            transform.position += transform.forward * speed * Time.deltaTime;
    }

    void OnTriggerEnter(Collider other)
    {
        // TODO: add impact handling, damage, explosion VFX, and filtering by layer/tag
        Destroy(gameObject);
    }
}