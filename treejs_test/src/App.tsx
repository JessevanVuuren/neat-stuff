import { Canvas } from '@react-three/fiber';
import './App.css';
import Screen from './Screen';
import { useRef, useState } from 'react';


export default function App() {
  const [best, setBest] = useState(0)
  return (
    <>
      <h1>ThreeJS React App - {best}</h1>
      <div id="screen">
        <Canvas orthographic camera={{ zoom: 1, position: [0, 0, 1] }} 
        onCreated={({ camera, size }) => {
          const { width, height } = size
          camera.left = 0
          camera.right = width
          camera.top = 0
          camera.bottom = -height
          camera.updateProjectionMatrix()
        }}>
          <Screen best_fitness={() => setBest(best+1)}/>
        </Canvas>
      </div>
    </>
  );
}
