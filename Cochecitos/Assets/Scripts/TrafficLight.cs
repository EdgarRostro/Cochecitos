using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrafficLight : MonoBehaviour {
    GameObject redLight;
    GameObject yellowLight;
    GameObject greenLight;

    void Start(){
        redLight = transform.Find("Rojo/RedLight").gameObject;
        yellowLight = transform.Find("Amarillo/YellowLight").gameObject;
        greenLight = transform.Find("Verde/GreenLight").gameObject;
        this.toggleState("Green");
    } 

    void Update(){}

    public void toggleState(string newState){
        redLight.SetActive(newState == "Red");
        yellowLight.SetActive(newState == "Yellow");
        greenLight.SetActive(newState == "Green");
    }
}