using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

class CarData{
    float old_x;
    float old_y;
    float x;
    float y;
    List<bool> directionLight;
    bool isParked;
}
class CarDataList {
    List<CarData> cars;
}

class TrafficLightData{
    float x;
    float y;
    string state;
}

class TrafficLightDataList{
    List<TrafficLightData> trafficLights;
}

public class City : MonoBehaviour {
    string hostname = "localhost:8585";
    string initEndpoint = "/init";
    string updateEndpoint = "/update";
    string getCarsEndpoint = "/cars";
    string getTrafficLightsEndpoint = "/trafficlights";

    [SerializeField] int cars;
    [SerializeField] int timeLimit;

    [SerializeField] GameObject carGameObject, trafficLightGameObject;
    [SerializeField] float trafficLightHeight;
    List<GameObject> cars;
    CarDataList carsData;
    List<GameObject> trafficLights;
    TrafficLightDataList trafficLightsData;

    bool refreshed;
    int countStart;
    float timeToUpdate = 2.0f, dt, timer, totalTime;

    void Start(){
        cars = new List<GameObject>();
        carsData = new CarDataList();
        trafficLights = new List<GameObject>();
        trafficLightsData = new TrafficLightDataList();
        StartCoroutine(InitSimulation());
        refreshed = true;
        totalTime = 0;
        timer = 0;
        countStart = 0;
    }

    void Update(){
        if(totalTime > timeLimit){
            Debug.Log("Time is up!");
            StartCoroutine(Quit());
        }
        if(timer >= timeToUpdate){
            timer = 0;
            refreshed = false;
            StartCoroutine(UpdateSimulation());
        }
        float t = timer/timeToUpdate;
        // Smooth transition
        dt = t * t * (3f - 2f*t);
        if(refreshed && countStart >= 4){
            // Update cars
            for(int i = 0; i < cars.Count; i++){
                // Interpolation
                Vector3 interpolation = Vector3.Lerp(
                    new Vector3(carsData.cars[i].old_x, carsData.cars[i].old_y), 
                    new Vector3(carsData.cars[i].x, carsData.cars[i].y)
                );
                cars[i].transform.position = interpolation;
                // Get direction as vector substraction
                Vector3 direction = cars[i].transform.position - new Vector3(carsData.cars[i].old_x, carsData.cars[i].old_y);
                cars[i].transform.rotation = Quaternion.LookRotation(direction);
                // Get class
                cars[i].GetComponent<Car>().leftBlinkerOn = carsData.cars[i].directionLight[0];
                cars[i].GetComponent<Car>().rightBlinkerOn = carsData.cars[i].directionLight[1];
            }
            // Update streetlights
            for(int i = 0; i < trafficLights.Count; i++){
                string state = trafficLightsData.trafficLights[i].state;
            }


        }
    }

    IEnumerator InitSimulation(){
        WWWForm form = new WWWForm();
        form.addField("cars", cars.toString());
        form.addField("timeLimit", timeLimit.toString());
        UnityWebRequest www = UnityWebRequest.Post(hostname + initEndpoint);   
        yield return www.SendWebRequest();
        if(www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        } else {
            Debug.Log("Starting cars");
            StartCoroutine(StartCars());
            StartCoroutine(StartTrafficLights());
        }
    }

    IEnumerator StartCars(){
        UnityWebRequest www = UnityWebRequest.Get(hostname + getCarsEndpoint);
        yield return www.SendWebRequest();
        if(www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        } else {
            carsData = JsonUtility.FromJson<CarDataList>(www.downloadHandler.text);
            foreach(CarData data in carsData.cars){
                cars.Add(Instantiate(CarGameObject, new Vector3(data.x, data.y, 0), Quaternion.identity));
            }
            countStart++;
        }
    }

    IEnumerator StartTrafficLights(){
        UnityWebRequest www = UnityWebRequest.Get(hostname + getTrafficLightsEndpoint);
        yield return www.SendWebRequest();
        if(www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        } else {
            trafficLightsData = JsonUtility.FromJson<TrafficLightDataList>(www.downloadHandler.text);
            foreach(TrafficLightData data in trafficLightsData.trafficLights){
                trafficLights.Add(Instantiate(trafficLightGameObject, new Vector3(data.x, data.y, traffic), Quaternion.identity));
            }
        }
    }

    IEnumerator Step(){
        UnityWebRequest www = UnityWebRequest.Get(hostname + updateEndpoint);
        yield return www.SendWebRequest();
        if(www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        } else {
            Debug.Log("Exito");
            if(www.downloadHandler.text == "False"){
                StartCoroutine(Quit());
            } else {
                StartCoroutine(GetCarsData());
                StartCoroutine(GetTrafficLightsData());
            }
        }
        refreshed = true;
    }

    IEnumerator GetCarsData(){
        UnityWebRequest www = UnityWebRequest.Get(hostname + getCarsEndpoint);
        yield return www.SendWebRequest();
        if(www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        } else {
            CarDataList _carsData = JsonUtility.FromJson<CarDataList>(www.downloadHandler.text);
            for(int i = 0; i < carsData.Count; i++){
                _carsData[i].old_x = carsData[i].x;
                _carsData[i].old_y = carsData[i].y;
                carsData[i] = _carsData[i];
            }
            countStart++;
        }
    }

    IEnumerator GetTrafficLightsData(){
        UnityWebRequest www = UnityWebRequest.Get(hostname + getTrafficLightsEndpoint);
        yield return www.SendWebRequest();
        if(www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        } else {
            trafficLightsData = JsonUtility.FromJson<TrafficLightDataList>(www.downloadHandler.text);
        }
    }

    IEnumerator Quit(){
        Debug.Log("Quitting. Missing final statistics");
    }

}