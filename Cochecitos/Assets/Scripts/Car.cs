using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Car : MonoBehaviour {
    GameObject leftBlinker;
    GameObject rightBlinker;

    GameObject frontLightA;
    GameObject frontLightB;
    void Start(){
        leftBlinker = transform.Find("Carroceria/LeftBlinker").gameObject;
        rightBlinker = transform.Find("Carroceria/RightBlinker").gameObject;
        frontLightA = transform.Find("Carroceria/FrontLightLeft").gameObject;
        frontLightB = transform.Find("Carroceria/FrontLightRight").gameObject;

        // this.toggleLeftBlinker(true);
        this.toggleFrontLights(true);
    }

    public void toggleLeftBlinker(bool newState){
        leftBlinker.SetActive(newState);
    }
    public void toggleRightBlinker(bool newState){
        rightBlinker.SetActive(newState);
    }
    public void toggleFrontLights(bool newState){
        frontLightA.SetActive(newState);
        frontLightB.SetActive(newState);
    }
}