import React, {useEffect, useState} from 'react';
import axios from 'axios';
import "./App.css";



const API_URL = "http://127.0.0.1:5000/artist";
const API_TEST = "https://jsonplaceholder.typicode.com/users"

function App() {

  const [searchTerm, setSearchTerm] = useState(""); 

  console.log("sexo");

  const searchArtist = async(artist) => {
    try {
      console.log("hola")
      // const response = await fetch(`${API_URL}/${artist}`);
      const response = await fetch(API_TEST);
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.log(artist);
      console.error(error);
    }

    // fetch(API_URL)
    // .then((response) => {
    //   return response.json();
    // })
    // .then((json) => {
    //   console.log(json);
    // });

    

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


      </div>
    );
  };
  
  export default App;