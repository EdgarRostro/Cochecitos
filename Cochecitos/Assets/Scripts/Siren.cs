using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Siren : MonoBehaviour
{
    [SerializeField] public bool isLightOn;
    // Start is called before the first frame update
    void Start()
    {
        isLightOn = false;
    }

    // Update is called once per frame
    void Update()
    {
        if(isLightOn){
            GetComponent<Renderer>().material.setColor("_TintColor", new Color(255, 0, 0, 179/255));
            GameObject.Find("PointLight").GetComponent<Light>().enabled = true;
        } else {
            GetComponent<Renderer>().material.setColor("_TintColor", new Color(1, 1, 0, 179/255));
            GameObject.Find("PointLight").GetComponent<Light>().enabled = false;
        }
    }

    void turnOn(){
        isLightOn = true;   
    }
    void turnOff(){
        isLightOn = false;
    }
}
