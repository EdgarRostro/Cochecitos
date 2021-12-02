using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CityMaker : MonoBehaviour
{
    [SerializeField] TextAsset layout;
    [SerializeField] GameObject callePrefab;
    [SerializeField] GameObject edificioPrefab;
    [SerializeField] GameObject semaforoPrefab;
    [SerializeField] GameObject crucePrefab;
    [SerializeField] GameObject destinoPrefab;
    [SerializeField] GameObject cochecitoPrefab;
    [SerializeField] int tileSize;

    List<GameObject> trafficLights;

    // Alternative syntax.
    Color[] coloresCochecito = {Color.red, Color.green, Color.blue, Color.yellow};
    
    // Start is called before the first frame update
    void Start()
    {
        trafficLights = new List<GameObject>();
        MakeTiles(layout.text);

        transform.GetComponent<City>().trafficLights = this.trafficLights;
        transform.GetComponent<City>().__StartSimulation();

    }

    // Update is called once per frame
    void Update()
    {
        transform.GetComponent<City>().__Update();
    }

    void MakeTiles(string tiles)
    {
        int x = 0;
        // Mesa has y 0 at the bottom
        // To draw from the top, find the rows of the file
        // and move down
        // Remove the last enter, and one more to start at 0
        int y = tiles.Split('\n').Length - 2;
        Debug.Log(y);

        Vector3 position;
        GameObject tile;

        for (int i=0; i<tiles.Length; i++) {
            if (tiles[i] == '>' || tiles[i] == '<') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(callePrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'v' || tiles[i] == '^') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(callePrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            } else if(tiles[i] == '⋝' || tiles[i] == '≥' || tiles[i] == '≤' || tiles[i] == '⋜'){
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(crucePrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'ú') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(semaforoPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                trafficLights.Add(tile);
                x += 1;
            } else if (tiles[i] == 'ù') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(semaforoPrefab, position, Quaternion.Euler(0, 270, 0));
                tile.transform.parent = transform;
                trafficLights.Add(tile);
                x += 1;
            } else if (tiles[i] == 'Ǔ') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(semaforoPrefab, position, Quaternion.Euler(0, 180, 0));
                tile.transform.parent = transform;
                trafficLights.Add(tile);
                x += 1;
            } else if (tiles[i] == 'Û') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(semaforoPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                trafficLights.Add(tile);
                x += 1;
            } else if (tiles[i] == 'D') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(destinoPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '#') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(edificioPrefab, position, Quaternion.identity);
                tile.transform.localScale = new Vector3(1, Random.Range(2.5f, 5.0f), 1);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'T') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(cochecitoPrefab, position, Quaternion.identity);
                tile.GetComponentInChildren<Renderer>().materials[0].color = coloresCochecito[Random.Range(0, coloresCochecito.Length)];   //Color.red;
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '\n') {
                x = 0;
                y -= 1;
            }
        }

    }
}
