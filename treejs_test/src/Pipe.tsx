import "./App.css"

const vert = `
varying vec2 vUv;
void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
`

const freg = `
varying vec2 vUv;

vec4 dark = vec4(0.098, 0.431, 0.055, 1.0);
vec4 light = vec4(0.227, 0.929, 0.137, 1.0);

void main() {
    float center_pos = 0.5;
    vec4 col = mix(mix(dark, light, vUv.x/center_pos), mix(light, dark, (vUv.x - center_pos)/(1.0 - center_pos)), step(center_pos, vUv.x));
    gl_FragColor = col;
}
`

const freg2 = `
varying vec2 vUv;

vec4 dark = vec4(0.0, 0.0, 0.0, 0.5);
vec4 light = vec4(0.0, 0.0, 0.0, 0.0);

void main() {
    float center_pos = 0.5;
    vec4 col = mix(dark, light, vUv.y);
    gl_FragColor = col;
}
`
interface PipeProps {
  position: { x: number, y: number, z: number }
  flipped: boolean
}


export default function Pipe(props: PipeProps) {

  return (
    <>
      <mesh position={[props.position.x + 0, props.position.y + (props.flipped ? -380 : 380), props.position.z + 0]}>
        <planeGeometry args={[100, 700]} />
        <shaderMaterial
          attach="material"
          vertexShader={vert}
          fragmentShader={freg}
        />
      </mesh>

      <mesh position={[props.position.x + 0, props.position.y + (props.flipped ? -42.5 : 42.5), props.position.z + 0]} rotation={[0, 0, +props.flipped && Math.PI]} >
        <planeGeometry args={[100, 25]} />
        <shaderMaterial
          transparent={true}
          attach="material"
          vertexShader={vert}
          fragmentShader={freg2}
        />
      </mesh>

      <mesh position={[props.position.x + 0, props.position.y + (props.flipped ? -15 : 15), props.position.z + 0]}>
        <planeGeometry args={[130, 30]} />
        <shaderMaterial
          transparent={true}
          attach="material"
          vertexShader={vert}
          fragmentShader={freg}
        />
      </mesh>
    </>


  )
}

