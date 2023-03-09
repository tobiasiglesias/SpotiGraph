import React, {useEffect, useRef, useState, createRef} from 'react';
import miserablesJson from './miserables.json'
import ForceGraph from './forceGraph';

function GraphView() {

    const miserables = miserablesJson;
    const chart = ForceGraph(miserables, {
        nodeId: (d) => d.id,
        nodeGroup: (d) => d.group,
        linkStrokeWidth: (l) => Math.sqrt(l.value),  
        width: 1200,
        height: 600,// a promise to stop the simulation when the cell is re-run
      })
      
      const svg = useRef(null);
      useEffect(()=>{
        if(svg.current){
          svg.current.appendChild(chart)
        } 
      }, []);
      
    if (chart.simulation && chart.simulation.restart) {chart.simulation.restart();}

    return ( 

      <div className='d-flex justify-content-center' ref={svg}></div>

     );
}

export default GraphView;