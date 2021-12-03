using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

[Serializable] // https://stackoverflow.com/a/41787127/2276332
class CarData
{
    // public float old_x;
    // public float old_y;
    public float x;
    public float y;
    public int directionLightLeft;
    public int directionLightRight;
    public bool isParked;
    /*     public CarData(){
            this.x = 0;
            this.y = 0;
            this.directionLightLeft = 0;
            this.directionLightRight = 0;
            this.isParked = false;
        } */
}

class CarDataList
{
    // public List<CarData> cars = new List<CarData>();
    public List<Vector3> oldPositions;
    public List<Vector3> positions;
    public List<int> directionLightLeft;
    public List<int> directionLightRight;
    public List<bool> isParked;
}

public class TrafficLightDataList
{
    public List<string> states;
}

public class City : MonoBehaviour
{
    string hostname = "localhost:8080";
    string initEndpoint = "/init";
    string updateEndpoint = "/update";
    string getCarsEndpoint = "/cars";
    string getTrafficLightsEndpoint = "/trafficlights";

    [SerializeField] int amountOfCars;
    [SerializeField] int timeLimit;

    [SerializeField] GameObject carGameObject;
    [SerializeField] Text info;
    List<GameObject> cars;
    CarDataList carsData;
    public List<GameObject> trafficLights;
    public TrafficLightDataList trafficLightsData;
 
    Color[] coloresCochecito = {Color.red, Color.green, Color.blue, Color.yellow};

    bool refreshed;
    int countStart;
    float timeToUpdate = 2.0f, dt, timer, totalTime;


    Vector3 position;
    Vector3 rotation;
    [SerializeField] GameObject view;
    Transform parent;
    bool car = false; 

    void Start()
    {
        cars = new List<GameObject>();
        carsData = new CarDataList();
        // trafficLights = new List<GameObject>();
        // trafficLightsData = new TrafficLightDataList();
        refreshed = true;
        totalTime = 0;
        timer = 0;
        countStart = 0;
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space) || Input.touchCount > 0){
            if (car){
                view.transform.parent = null;
                position = new Vector3(12.5f, 18.5f, 12.5f);
                view.transform.localPosition = position;
                view.transform.localRotation = Quaternion.Euler(90.0f, 0.0f, 0.0f);
                car = false;
            }
            else{
                parent = cars[UnityEngine.Random.Range(0, cars.Count)].GetComponent<Transform>();
                view.transform.SetParent(parent);
                position = new Vector3(0.0f, 1.0f, -1.4f);
                view.transform.localPosition = position;
                view.transform.localRotation = Quaternion.identity;
                car = true;
            }
        }
    }

    public void __StartSimulation()
    {
        StartCoroutine(InitSimulation());
    }

    public void __Update()
    {
        if (totalTime > timeLimit)
        {
            Debug.Log("Time is up!");
            StartCoroutine(Quit());
        }
        if (timer >= timeToUpdate)
        {
            timer = 0;
            refreshed = false;
            StartCoroutine(Step());
        }
        float t = timer / timeToUpdate;
        // Smooth transition
        // dt = t * t * (3f - 2f * t);
        dt = t;
        Debug.Log("Refreshed is " + refreshed);
        Debug.Log("CountStart is " + countStart);
        if (refreshed && countStart >= 1 && cars.Count == amountOfCars)
        {
            // Update cars
            for(int i = 0; i < amountOfCars; i++){
                // Interpolation
                Vector3 interpolation = Vector3.Lerp(cars[i].transform.position, carsData.positions[i], dt);
                cars[i].transform.position = interpolation;
                // Direction
                Vector3 direction = carsData.positions[i] - carsData.oldPositions[i];
                // cars[i].transform.rotation = Quaternion.LookRotation(direction);
                cars[i].transform.rotation = Quaternion.Lerp(cars[i].transform.rotation, Quaternion.LookRotation(direction), dt);
                // Direction lights
                cars[i].GetComponent<Car>().toggleLeftBlinker(carsData.directionLightLeft[i] == 1);
                cars[i].GetComponent<Car>().toggleRightBlinker(carsData.directionLightRight[i] == 1);
            }
            // Update streetlights
            for (int i = 0; i < trafficLights.Count; i++){
                string state = trafficLightsData.states[i];
                Debug.Log("Traffic light is now " + state);
                trafficLights[i].transform.Find("Calle/TrafficLight").GetComponent<TrafficLight>().toggleState(state);
            }
        }
        timer += Time.deltaTime;
        totalTime += Time.deltaTime;
    }

    IEnumerator InitSimulation()
    {
        WWWForm form = new WWWForm();
        form.AddField("cars", amountOfCars.ToString());
        form.AddField("timeLimit", timeLimit.ToString());
        UnityWebRequest www = UnityWebRequest.Post(hostname + initEndpoint, form);
        yield return www.SendWebRequest();
        if (www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        }
        else{
            Debug.Log("Starting cars");
            StartCoroutine(StartCars());
        }
    }

    IEnumerator StartCars()
    {
        UnityWebRequest www = UnityWebRequest.Get(hostname + getCarsEndpoint);
        yield return www.SendWebRequest();
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log("Error al empezar coches");
            Debug.Log(www.error);
        }
        else
        {

            // CarData d = JsonUtility.FromJson<CarData>(www.downloadHandler.text); 
            carsData = JsonUtility.FromJson<CarDataList>(www.downloadHandler.text);
            carsData.oldPositions = carsData.positions;
            for (int i = 0; i < amountOfCars; i++)
            {
                GameObject car = Instantiate(carGameObject, carsData.positions[i], Quaternion.identity);
                car.GetComponentInChildren<Renderer>().materials[0].color = coloresCochecito[UnityEngine.Random.Range(0, coloresCochecito.Length)];
                cars.Add(car);
                car.transform.parent = transform; 
            }
            countStart++;
        }
    }

    IEnumerator Step()
    {
        UnityWebRequest www = UnityWebRequest.Get(hostname + updateEndpoint);
        yield return www.SendWebRequest();
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            if (www.downloadHandler.text == "False")
            {
                StartCoroutine(Quit());
            }
            else
            {
                StartCoroutine(GetCarsData());
                StartCoroutine(GetTrafficLightsData());
            }
        }
        refreshed = true;
    }

    IEnumerator GetCarsData()
    {
        UnityWebRequest www = UnityWebRequest.Get(hostname + getCarsEndpoint);
        yield return www.SendWebRequest();
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            CarDataList newCarsData = JsonUtility.FromJson<CarDataList>(www.downloadHandler.text);
            newCarsData.oldPositions = carsData.positions;
            carsData = newCarsData;
        }
    }

    IEnumerator GetTrafficLightsData()
    {
        UnityWebRequest www = UnityWebRequest.Get(hostname + getTrafficLightsEndpoint);
        yield return www.SendWebRequest();
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            trafficLightsData = JsonUtility.FromJson<TrafficLightDataList>(www.downloadHandler.text);
        }
    }

    IEnumerator Quit()
    {
        Debug.Log("Quitting. Missing final statistics");
        UnityWebRequest www = UnityWebRequest.Get(hostname + "/finalstats");
        yield return www.SendWebRequest();
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            TrafficLightDataList finalStats;
            finalStats = JsonUtility.FromJson<TrafficLightDataList>(www.downloadHandler.text);
            transform.GetComponent<CityMaker>().running = false;
            info.text = "SIMULACIÓN TERMINADA\nCoches estacionados: "+finalStats.states[0]+"\nMovimientos totales: "+finalStats.states[1];
        }
    }

}