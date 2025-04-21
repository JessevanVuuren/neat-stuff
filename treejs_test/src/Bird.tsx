import { useFrame, useLoader } from "@react-three/fiber"
import { RefObject, useEffect, useState } from "react"
import { Mesh, TextureLoader } from "three"

interface BirdProps {
  ref: RefObject<Mesh>
  speed:number
}


const Bird = (props: BirdProps) => {
  const [keyWDown, setKeyWDown] = useState(false)
  const [keySDown, setKeySDown] = useState(false)

  useEffect(() => {
    window.addEventListener("keydown", (e) => {
      if (e.key == "w") setKeyWDown(true)
      if (e.key == "s") setKeySDown(true)
    })
    window.addEventListener("keyup", (e) => {
      if (e.key == "w") setKeyWDown(false)
      if (e.key == "s") setKeySDown(false)
    })
  }, [])

  useFrame((_, delta) => {
    if (keySDown) props.ref.current.position.y -= delta * props.speed
    if (keyWDown) props.ref.current.position.y += delta * props.speed
  })

  const birdTexture = useLoader(TextureLoader, "./bird.png")


  return (
    <>
      <mesh ref={props.ref} position={[300, 0, 0]}>
        <planeGeometry args={[100, 100]} />
        <meshBasicMaterial map={birdTexture} transparent />
      </mesh>
    </>
  )
}

export default Bird
