using UnityEngine;

/// <summary>
/// Basic ship controller for 3D ship model. Uses Rigidbody for physics-based movement,
/// supports rotation, forward thrust and fire. Fire spawns projectile prefab and uses object pooling where available.
/// </summary>
[RequireComponent(typeof(Rigidbody))]
public class ShipController : MonoBehaviour
{
    public float thrustForce = 20f;
    public float rotationSpeed = 90f; // degrees per second
    public GameObject projectilePrefab;
    public Transform firePoint;
    public float fireCooldown = 0.2f;

    private Rigidbody rb;
    private float lastFireTime;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
        rb.useGravity = false;
        rb.drag = 0.5f;
    }

    void Update()
    {
        // Rotation (yaw)
        float yaw = Input.GetAxis("Horizontal");
        transform.Rotate(Vector3.up, yaw * rotationSpeed * Time.deltaTime, Space.Self);

        // Thrust (forward/back)
        if (Input.GetKey(KeyCode.W) || Input.GetKey(KeyCode.UpArrow))
        {
            rb.AddForce(transform.forward * thrustForce, ForceMode.Acceleration);
        }
        if (Input.GetKey(KeyCode.S) || Input.GetKey(KeyCode.DownArrow))
        {
            rb.AddForce(-transform.forward * (thrustForce * 0.5f), ForceMode.Acceleration);
        }

        // Fire
        if ((Input.GetKey(KeyCode.Space) || Input.GetButton("Fire1")) && Time.time - lastFireTime >= fireCooldown)
        {
            Fire();
            lastFireTime = Time.time;
        }
    }

    void Fire()
    {
        if (projectilePrefab == null || firePoint == null) return;

        // Instantiate — replace with pooling when available
        GameObject proj = Instantiate(projectilePrefab, firePoint.position, firePoint.rotation);
        Rigidbody prb = proj.GetComponent<Rigidbody>();
        if (prb != null)
        {
            // give projectile initial velocity (inherit ship velocity)
            prb.velocity = rb.velocity + transform.forward * 80f;
        }
    }
}