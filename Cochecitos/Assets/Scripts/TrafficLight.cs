using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrafficLight : MonoBehaviour {
    public string state;
    GameObject redLight;
    GameObject greenLight;
    GameObject yellowLight;

    void Start(){
    }

    void Update(){}

    void toggleState(string newState){
        if(newState == state) return;
        if(newState == "Red"){
            Debug.Log("I am red");
        } else if(newState == "Green"){
            Debug.Log("I am green");
        } else if(newState == "Yellow"){
            Debug.Log("I am yellow");
        }
    }
}