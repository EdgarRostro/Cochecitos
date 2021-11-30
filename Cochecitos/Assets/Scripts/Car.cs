using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Car : MonoBehaviour {
    public bool leftBlinkerOn;
    public bool rightBlinkerOn;

    void Start(){
        leftBlinkerOn = false;
        rightBlinkerOn = false;
    }

    void toggleLeftBlinker(bool newState){
        if(newState == leftBlinkerOn) return;
        if(newState == true){
            Debug.Log("Left blinker is on");
        } else {
            Debug.Log("Left blinker is off");
        }
        leftBlinkerOn = newState;
    }
    void toggleRightBlinker(bool newState){
        if(newState == rightBlinkerOn) return;
        if(newState == true){
            Debug.Log("Right blinker is on");
        } else {
            Debug.Log("Right blinker is off");
        }
        rightBlinkerOn = newState;
    }
}