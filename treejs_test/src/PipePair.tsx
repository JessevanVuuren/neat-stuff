import { RefCallback } from "react"
import { Group } from "three"
import Pipe from "./Pipe"

interface PipePairProps {
  ref: RefCallback<Group>
  gap_size:number
  gap_pos:number
}

const PipePair = (props: PipePairProps) => {

  const pipe_up = { x: 1400, y: 0, z: 0 };
  const pipe_down = { x: 1400, y: 0, z: 0 }

  pipe_up.y = -props.gap_pos
  pipe_down.y = -props.gap_pos - props.gap_size

  return (
    <group ref={props.ref}>
      <Pipe position={pipe_up} flipped={false} />
      <Pipe position={pipe_down} flipped={true} />
    </group>
  )
}

export default PipePair
