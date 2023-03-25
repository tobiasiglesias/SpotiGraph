import React, {useEffect, useState} from 'react';
import GraphView from './GraphView';
import "./App.css";



const API_URL = "http://127.0.0.1:5000/artist/collabs";
// const API_URL = "http://127.0.0.1:8080/artist/collabs";

function App() {

  const [graphData, setGraphData] = useState();
  const [searchTerm, setSearchTerm] = useState("");
  var gData = undefined;
  var mainArtist = undefined;
  const [finishedFetching, setFinishedFetching] = useState(false);

  function addGraphData(currentNodes, currentLinks, newNodes, newLinks){
  
    // Agregar nuevos nodos sin duplicados
    const nodesToAdd = newNodes.filter(node => !currentNodes.find(n => n.id === node.id));
    const updatedNodes = currentNodes.concat(nodesToAdd);
  
    // Agregar nuevos enlaces sin duplicados
    const linksToAdd = newLinks.filter(link => !currentLinks.find(l => l.source === link.source && l.target === link.target));
    const updatedLinks = currentLinks.concat(linksToAdd);
  
    return ({
      nodes: updatedNodes,
      links: updatedLinks
    });


};




  const searchCollabs = async(artist) => {
    try {
      const response = await fetch(`${API_URL}/${artist}`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(error);
      return null; // o return {nodes: [], links: []};
    }
  };

  const getCompleteGraph = (artist) => {
    const data = searchCollabs(artist);
    data.then(response => {
      mainArtist = response;
      gData = addGraphData([], [], mainArtist.nodes, mainArtist.links);
      getAllCollabs();
    });


   }

  
  function getAllCollabs(){
    var data = [];

    mainArtist.nodes.forEach(node => {

      if (!node.main_artist && data.length < 50){
        node.main_artist = true;
        data.push(searchCollabs(node.name));
      };
    });

    Promise.allSettled(data).
    then(results => {
      results.forEach(response => {
        gData = addGraphData(gData.nodes, gData.links, response.value.nodes, response.value.links);
      } );
      setFinishedFetching(true);
      setGraphData(gData);
    });

  };




    return (
      <div className="app">
        <div className='d-flex justify-content-center'>
          <h1 className="text-primary p-3">SpotiGraph</h1>
          <h3 className='text-danger pt-3'>prototipo</h3>
        </div>
  
        <div className='d-flex justify-content-center'>
            <nav className="navbar bg-body-tertiary">
              <div className="container-fluid">
                  <div className="d-flex" role="search">
                  <input
                      className="form-control form-control-lg me-2"
                      type="search"
                      placeholder="Search artist"
                      aria-label="Search"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}

                  />
                  <button className="btn btn-outline-success ml-2" type="submit" onClick={() => getCompleteGraph(searchTerm)}>
                      Search
                  </button>
                  </div>

              </div>
            </nav>
        </div>

        <div>
          {finishedFetching === true ? <GraphView graphData={graphData}>test</GraphView> : null}

        </div>


      </div>
    );
  };
  
  export default App;