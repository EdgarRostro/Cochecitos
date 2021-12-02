using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

class CarData{
    // public float old_x;
    // public float old_y;
    public float x;
    public float y;
    public int directionLightLeft;
    public int directionLightRight;
    public bool isParked;
    public CarData(){
        this.x = 0;
        this.y = 0;
        this.directionLightLeft = 0;
        this.directionLightRight = 0;
        this.isParked = false;
    }
}
class CarDataList {
    public CarData[] cars;
    public CarDataList(int n){
        cars = new CarData[n];
        for(int i = 0; i < n; i++) cars[i] = new CarData();
    }
}

class TrafficLightData{
    public float x;
    public float y;
    public string state;
}

class TrafficLightDataList{
    public List<TrafficLightData> trafficLights;
}

public class City : MonoBehaviour {
    string hostname = "localhost:8585";
    string initEndpoint = "/init";
    string updateEndpoint = "/update";
    string getCarsEndpoint = "/cars";
    string getTrafficLightsEndpoint = "/trafficlights";

    [SerializeField] int amountOfCars;
    [SerializeField] int timeLimit;

    [SerializeField] GameObject carGameObject;
    List<GameObject> cars;
    CarDataList carsData;
    public List<GameObject> trafficLights;
    TrafficLightDataList trafficLightsData;

    bool refreshed;
    int countStart;
    float timeToUpdate = 2.0f, dt, timer, totalTime;

    void Start(){
        cars = new List<GameObject>();
        carsData = new CarDataList(amountOfCars);
        trafficLights = new List<GameObject>();
        trafficLightsData = new TrafficLightDataList();
        refreshed = true;
        totalTime = 0;
        timer = 0;
        countStart = 0;
    }

    public void __StartSimulation(){
        StartCoroutine(InitSimulation());
    }

    public void __Update(){
        if(totalTime > timeLimit){
            Debug.Log("Time is up!");
            StartCoroutine(Quit());
        }
        if(timer >= timeToUpdate){
            timer = 0;
            refreshed = false;
            StartCoroutine(Step());
        }
        float t = timer/timeToUpdate;
        // Smooth transition
        dt = t * t * (3f - 2f*t);
            Debug.Log("Refreshed is " + refreshed);
            Debug.Log("CountStart is " + countStart);
        if(refreshed && countStart >= 1){
            Debug.Log("Updating something here");
            // Update cars
            /* for(int i = 0; i < cars.Count; i++){
                // Interpolation
                Vector3 interpolation = Vector3.Lerp(
                    new Vector3(carsData.cars[i].old_x, 0, carsData.cars[i].old_y), 
                    new Vector3(carsData.cars[i].x, 0, carsData.cars[i].y),
                    dt
                );
                cars[i].transform.position = interpolation;
                // Get direction as vector substraction
                Vector3 direction = cars[i].transform.position - new Vector3(carsData.cars[i].old_x, carsData.cars[i].old_y);
                cars[i].transform.rotation = Quaternion.LookRotation(direction);
                // Get class
                cars[i].GetComponent<Car>().toggleLeftBlinker(carsData.cars[i].directionLight[0] == 1);
                cars[i].GetComponent<Car>().toggleRightBlinker(carsData.cars[i].directionLight[1] == 1);
            }  */
            // Update streetlights
            for(int i = 0; i < trafficLights.Count; i++){
                string state = trafficLightsData.trafficLights[i].state;
                // TODO: Integrar con los semáforos de CityMaker.cs
                trafficLights[i].GetComponent<TrafficLight>().toggleState(state);
            }
        }
        timer += Time.deltaTime;
        totalTime += Time.deltaTime;
    }

    IEnumerator InitSimulation(){
        WWWForm form = new WWWForm();
        form.AddField("cars", amountOfCars.ToString());
        form.AddField("timeLimit", timeLimit.ToString());
        UnityWebRequest www = UnityWebRequest.Post(hostname + initEndpoint, form);   
        yield return www.SendWebRequest();
        if(www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        } else {
            Debug.Log("Starting cars");
            StartCoroutine(StartCars());
        }
    }

    IEnumerator StartCars(){
        UnityWebRequest www = UnityWebRequest.Get(hostname + getCarsEndpoint);
        yield return www.SendWebRequest();
        if(www.result != UnityWebRequest.Result.Success){
            Debug.Log("Error al empezar coches");
            Debug.Log(www.error);
        } else {
            carsData = JsonUtility.FromJson<CarDataList>(www.downloadHandler.text);
            Debug.Log("Download...");
            Debug.Log(www.downloadHandler.text);
            // for(int i = 0; i < carsData.cars.Count; i++){
                /* GameObject car = Instantiate(carGameObject, new Vector3(data.x, 0, data.y), Quaternion.identity);
                cars.Add(car);
                car.transform.parent = transform; */
            // }
            countStart++;
        }
    }

    IEnumerator Step(){
        UnityWebRequest www = UnityWebRequest.Get(hostname + updateEndpoint);
        yield return www.SendWebRequest();
        if(www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        } else {
            if(www.downloadHandler.text == "False"){
                StartCoroutine(Quit());
            } else {
                // StartCoroutine(GetCarsData());
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
            for(int i = 0; i < carsData.cars.Length; i++){
                // _carsData.cars[i].old_x = carsData.cars[i].x;
                // _carsData.cars[i].old_y = carsData.cars[i].y;
                carsData.cars[i] = _carsData.cars[i];
            }
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
        UnityWebRequest www = UnityWebRequest.Get(hostname + "/finalstats");
        yield return www.SendWebRequest();
    }

}