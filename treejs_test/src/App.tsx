import { Canvas } from '@react-three/fiber';
import './App.css';
import Screen from './Screen';


export default function App() {
  return (
    <>
      <h1>ThreeJS React App</h1>
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
          <Screen />
        </Canvas>
      </div>
    </>
  );
}
