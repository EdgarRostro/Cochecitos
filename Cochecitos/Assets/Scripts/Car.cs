using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Car : MonoBehaviour {
    GameObject leftBlinker;
    GameObject rightBlinker;

    GameObject frontLightA;
    GameObject frontLightB;
    void Start(){
        leftBlinker = transform.Find("LeftBlinker").gameObject;
        rightBlinker = transform.Find("RightBlinker").gameObject;
        frontLightA = transform.Find("FrontLightLeft").gameObject;
        frontLightB = transform.Find("FrontLightRight").gameObject;

        this.toggleLeftBlinker(true);
    }

    public void toggleLeftBlinker(bool newState){
        Debug.Log("Semaforo ahora es " + newState);
        leftBlinker.SetActive(newState);
    }
    public void toggleRightBlinker(bool newState){
        Debug.Log("Semaforo ahora es " + newState);
        rightBlinker.SetActive(newState);
    }
    public void toggleFrontLights(bool newState){
        frontLightA.SetActive(newState);
        frontLightB.SetActive(newState);
    }
}