import React, {useEffect, useState} from 'react';
import GraphView from './GraphView';
import "./App.css";



const API_URL = "http://127.0.0.1:5000/artist/collabs";

function App() {

  const [searchTerm, setSearchTerm] = useState("");
  const [artist, setArtist] = useState(null);

  console.log("sexo");

  const searchArtist = async(artist) => {
    setArtist(null)
    try {
      console.log("hola")
      const response = await fetch(`${API_URL}/${artist}`);
      const data = await response.json();
      setArtist(data);
    } catch (error) {
      console.error(error);
    }

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
                  <button className="btn btn-outline-success ml-2" type="submit" onClick={() => searchArtist(searchTerm)}>
                      Search
                  </button>
                  </div>
                  
              </div>
            </nav>
        </div>

        <div>
          {artist != null ? <GraphView gData={artist}>test</GraphView> : null}

        </div>


      </div>
    );
  };
  
  export default App;