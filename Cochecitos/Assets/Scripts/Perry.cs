using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Perry : MonoBehaviour
{
    [SerializeField] public GameObject siren;
    [SerializeField] public bool isSirenOn;
    // Start is called before the first frame update
    void Start()
    {
        isSirenOn = false;
        siren = GameObject.Find("Siren");
    }

    // Update is called once per frame
    void Update()
    {
        if(isSirenOn){
            siren.GetComponent<Siren>().turnOn();
        } else {
            siren.GetComponent<Siren>().turnOff();
        }
    }

    public void turnOn(){
        isSirenOn = true;
        siren.GetComponent<Siren>().turnOn();
    }

    public void turnOff(){
        isSirenOn = false;
        siren.GetComponent<Siren>().turnOff();
    }

}
 