import React, {useState} from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import * as THREE from 'three';
function GraphView(props) {
    const [graphData, setGraphData] = useState(props.gData)

    const nodes = graphData.nodes
    const links = graphData.links

    nodes.forEach(node => {console.log(node)})

    return ( 
        <ForceGraph3D
        graphData={graphData}
        nodeThreeObject={({ image_url }) => {
          const imgTexture = new THREE.TextureLoader().load(image_url);
          const material = new THREE.SpriteMaterial({ map: imgTexture });
          const sprite = new THREE.Sprite(material);
          sprite.scale.set(12, 12);

          return sprite;
        }}
      />
     );
}

export default GraphView;