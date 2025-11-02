using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Simple object pool for repeated projectiles/FX to avoid runtime allocations.
/// Create one pool per prefab type (e.g., ProjectilePool) and call Get/Return.
/// </summary>
public class ObjectPool : MonoBehaviour
{
    public GameObject prefab;
    public int initialSize = 20;
    private Queue<GameObject> pool = new Queue<GameObject>();

    void Awake()
    {
        for (int i = 0; i < initialSize; i++)
        {
            GameObject o = Instantiate(prefab);
            o.SetActive(false);
            pool.Enqueue(o);
        }
    }

    public GameObject Get(Vector3 position, Quaternion rotation)
    {
        GameObject o;
        if (pool.Count > 0)
        {
            o = pool.Dequeue();
            o.transform.position = position;
            o.transform.rotation = rotation;
            o.SetActive(true);
            return o;
        }

        o = Instantiate(prefab, position, rotation);
        return o;
    }

    public void Return(GameObject o)
    {
        o.SetActive(false);
        pool.Enqueue(o);
    }
}