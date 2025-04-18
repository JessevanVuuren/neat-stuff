import { createRef, Dispatch, RefObject, SetStateAction, useEffect, useRef, useState } from "react"
import { useFrame, useLoader } from "@react-three/fiber"
import { Group, Mesh, TextureLoader } from "three"
import PipePair from "./PipePair"
import "./App.css"

const gap = 200
const speed = 2
const distance = 400

interface PipeObject {
  ref: RefObject<Group | null>,
  gap: number
}

const new_pipe = (pipes: PipeObject[], setPipes: Dispatch<SetStateAction<PipeObject[]>>) => {
  setPipes([...pipes, { gap: Math.random() * (720 - gap), ref: createRef() }])
}

const Screen = () => {
  const [pipes, setPipes] = useState<Array<PipeObject>>([])
  const last_pipe = useRef<Group>(null!)

  const velocity = useRef(0)
  const acceleration = useRef(-900)
  const bird = useRef<Mesh>(null!)


  const birdTexture = useLoader(TextureLoader, "./bird.png")
  

  useEffect(() => {
    window.addEventListener("keydown", (e) => {
      if (e.key == " ") {
        jump()
      }
    })
  }, [])

  useFrame((_, delta) => {
    pipes.forEach(pipe => {
      if (pipe.ref.current) {
        pipe.ref.current.position.x -= speed
      }
    })

    if (bird.current) {
      velocity.current += acceleration.current * delta
      bird.current.position.y += velocity.current * delta
    }

    if (pipes.length == 0) new_pipe(pipes, setPipes)

    if (last_pipe.current && last_pipe.current.position.x < -distance) {
      new_pipe(pipes, setPipes)
    }
  })

  const jump = () => {
    velocity.current = 500
  }

  return (
    <>
      <color attach="background" args={['#aaaaff']} />

      <mesh ref={bird} position={[300, -360, 0]}>
        <planeGeometry args={[100, 100]} />
        <meshBasicMaterial map={birdTexture} transparent />
      </mesh>

      {pipes.map((e, index) => {
        return <PipePair key={index} gap_size={gap} gap_pos={e.gap} ref={(r: Group) => {
          last_pipe.current = r
          e.ref.current = r
        }} />
      })}

    </>
  )
}

export default Screen

