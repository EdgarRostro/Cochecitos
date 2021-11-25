﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Perry : MonoBehaviour
{
    GameObject siren;
    bool isSirenOn;
    public string condition;
    // Start is called before the first frame update
    void Start()
    {
        isSirenOn = false;
        siren = transform.Find("Siren").gameObject;
    }

    // Update is called once per frame
    void Update()
    {
        if( condition == "Searching" ){
            turnOn();
        } else if (condition == "Placing"){
            turnOff();
        }
    }

    public void turnOn(){
        isSirenOn = true;
        Debug.Log("Turn on");
    
        siren.GetComponent<Renderer>().material.SetColor("_TintColor", new Color(1, 0, 0, 179/255));
        transform.Find("Siren/PointLight").gameObject.GetComponent<Light>().enabled = true;
    }

    public void turnOff(){
        isSirenOn = false;
        Debug.Log("Turn off");
        
        siren.GetComponent<Renderer>().material.SetColor("_TintColor", new Color(1, 1, 0, 179/255));
        transform.Find("Siren/PointLight").gameObject.GetComponent<Light>().enabled = false;
    }
}