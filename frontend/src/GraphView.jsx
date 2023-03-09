import React, {useEffect, useState} from 'react';
import miserablesJson from './miserables.json'
import ForceGraph from './forceGraph';

function GraphView() {

    const miserables = miserablesJson;
    const chart = ForceGraph(miserables, {
        nodeId: (d) => d.id,
        nodeGroup: (d) => d.group,
        linkStrokeWidth: (l) => Math.sqrt(l.value),  
        width: 600,
        height: 600,// a promise to stop the simulation when the cell is re-run
      })

    return ( 

        {chart}

     );
}

export default GraphView;