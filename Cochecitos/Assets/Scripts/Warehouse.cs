using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class AgentData {
    public List<Vector3> positions;
}

public class Warehouse : MonoBehaviour
{
    string url = "localhost:8585";
    string getRobotsEndpoint = "/getRobots";
    string getBoxesEndpoint = "/getBoxes";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    [SerializeField] int width;
    [SerializeField] int height;
    [SerializeField] float density;
    [SerializeField] int robotAmt;
    [SerializeField] float timer;
    float timeToUpdate = 2.0f, dt;
    [SerializeField] GameObject box, robot;
    List<GameObject> boxes;
    List<GameObject> robots;
    AgentData boxPositions;
    AgentData robotPositions;
    List<Vector3> oldBoxPos;
    List<Vector3> oldRobotPos;

    bool refreshed;

    // Start is called before the first frame update
    void Start()
    {
        boxPositions = new AgentData();
        robotPositions = new AgentData();
        boxes = new List<GameObject>();
        robots = new List<GameObject>();

        StartCoroutine(StartSimulation());
        refreshed = true;
        // timer = 1.0f;
    }

    // Update is called once per frame
    void Update()
    {
        if(timer >= timeToUpdate)
        {
            timer = 0;
            refreshed = false;
            StartCoroutine(UpdateSimulation());
        }
        float t = timer/timeToUpdate;
        // Smooth out the transition at start and end
        dt = t * t * ( 3f - 2f*t);

        if(refreshed) {
            // Update box position
            for(int i=0; i < boxes.Count; i++) {
                Vector3 interpolated = Vector3.Lerp(oldBoxPos[i], boxPositions.positions[i], dt);
                boxes[i].transform.position = interpolated;
            }
    
            // Update robot position and direction
            for(int i=0; i < robots.Count; i++) {
                Vector3 interpolated = Vector3.Lerp(oldRobotPos[i], robotPositions.positions[i], dt);
                robots[i].transform.position = interpolated;

                Vector3 dir = robots[i].transform.position - robotPositions.positions[i];
                robots[i].transform.rotation = Quaternion.LookRotation(dir);
            }
            // Move time from the last frame
            timer += Time.deltaTime;
        }

    }

    // Send parameters to API
    IEnumerator StartSimulation()
    {
        WWWForm form = new WWWForm();
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());
        form.AddField("density", density.ToString());
        form.AddField("robots", robotAmt.ToString());
        form.AddField("timer", timer.ToString());

        UnityWebRequest www = UnityWebRequest.Post(url+"/init", form);

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        }
        else {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(StartBoxes());
            StartCoroutine(StartRobots());
        }
    }

    // Create box objects
    IEnumerator StartBoxes() {
        UnityWebRequest www = UnityWebRequest.Get(url+getBoxesEndpoint);

        yield return www.SendWebRequest();
        if(www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        } else {
            boxPositions = JsonUtility.FromJson<AgentData>(www.downloadHandler.text);
            Debug.Log("Getting updated boxes");

            foreach(Vector3 position in boxPositions.positions) {
                boxes.Add(Instantiate(box, position, Quaternion.identity));
            }
        }
    }
    
    // Create robot objects
    IEnumerator StartRobots() {
        UnityWebRequest www = UnityWebRequest.Get(url+getRobotsEndpoint);

        yield return www.SendWebRequest();
        if(www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        } else {
            robotPositions = JsonUtility.FromJson<AgentData>(www.downloadHandler.text);
            Debug.Log("Getting updated robots");

            foreach(Vector3 position in robotPositions.positions) {
                robots.Add(Instantiate(robot, position, Quaternion.identity));
            }
        }
    }

    // Make a step in mesa simulation
    IEnumerator UpdateSimulation() {
        UnityWebRequest www = UnityWebRequest.Get(url+updateEndpoint);
        yield return www.SendWebRequest();
        if(www.result != UnityWebRequest.Result.Success) Debug.Log(www.error);
        else {
            Debug.Log("Exito");
            StartCoroutine(GetBoxPositions());
            StartCoroutine(GetRobotPositions());
        }
        refreshed = true;
    }

    IEnumerator GetBoxPositions(){
        UnityWebRequest www = UnityWebRequest.Get(url+getBoxesEndpoint);
        yield return www.SendWebRequest();
        if(www.result != UnityWebRequest.Result.Success) Debug.Log(www.error);
        else {
            oldBoxPos = new List<Vector3>(boxPositions.positions);
            boxPositions = JsonUtility.FromJson<AgentData>(www.downloadHandler.text);
        }
    }

    IEnumerator GetRobotPositions(){
        UnityWebRequest www = UnityWebRequest.Get(url+getRobotsEndpoint);
        yield return www.SendWebRequest();
        if(www.result != UnityWebRequest.Result.Success) Debug.Log(www.error);
        else {
            oldRobotPos = new List<Vector3>(robotPositions.positions);
            robotPositions = JsonUtility.FromJson<AgentData>(www.downloadHandler.text);
        }
    }
}
