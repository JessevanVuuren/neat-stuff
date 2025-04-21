import { createRef, Dispatch, RefObject, SetStateAction, useRef, useState } from "react"
import { Box2, Group, Mesh, Vector3, Vector2 } from "three"
import { useFrame } from "@react-three/fiber"
import PipePair from "./PipePair"
import Bird from "./Bird"
import "./App.css"

const gap = 200
const speed = 2
const distance = 1000

interface PipeObject {
  ref: RefObject<Group | null>,
  gap: number
  position: Vector3,
}

interface PipeBoundingBox {
  top: Box2
  bottom: Box2
}

const pipe_bounding_box = (pos: PipeObject): PipeBoundingBox => {
  const top_left_top = new Vector2(pos.position.x - 50, 0)
  const top_down_right = new Vector2(pos.position.x + 50, pos.gap)

  const down_left_top = new Vector2(pos.position.x - 50, pos.gap + gap)
  const down_down_right = new Vector2(pos.position.x + 50, 720)

  const top_pipe = new Box2(top_left_top, top_down_right)
  const down_pipe = new Box2(down_left_top, down_down_right)

  return { top: top_pipe, bottom: down_pipe }
}

const bird_bounding_box = (bird: Mesh): Box2 => {
  const top_left = new Vector2(bird.position.x - 50, Math.abs(bird.position.y) - 50)
  const down_right = new Vector2(bird.position.x + 50, Math.abs(bird.position.y) + 50)

  return new Box2(top_left, down_right)
}

const new_pipe = (pipes: PipeObject[], setPipes: Dispatch<SetStateAction<PipeObject[]>>) => {
  setPipes([...pipes, { gap: Math.random() * (720 - gap), ref: createRef(), position: new Vector3(1400, 0, 0) }])
}

interface ScreenProps {
  best_fitness: () => void;
}

const Screen = ({ best_fitness }: ScreenProps) => {
  const [pipes, setPipes] = useState<Array<PipeObject>>([])
  const last_pipe = useRef<Group>(null!)
  const bird = useRef<Mesh>(null!)
  const bird_time_alive = useRef(0)

  useFrame(() => {
    pipes.forEach(pipe => {
      if (pipe.ref.current) {
        pipe.position.x -= speed
        pipe.ref.current.position.x = pipe.position.x


        const box = pipe_bounding_box(pipe)
        const bird_box = bird_bounding_box(bird.current)
        if (box.top.intersectsBox(bird_box) || box.bottom.intersectsBox(bird_box)) {

          console.log("dead")
        }

        bird_time_alive.current++
        best_fitness()
      }


    })

    if (pipes.length == 0) new_pipe(pipes, setPipes)

    if (last_pipe.current && last_pipe.current.position.x < distance) {
      new_pipe(pipes, setPipes)
    }
  })

  return (
    <>
      <color attach="background" args={['#aaaaff']} />

      <Bird ref={bird} speed={500} />

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

