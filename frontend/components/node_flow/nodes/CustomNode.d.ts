import { NodeProps } from '@xyflow/react';


type CustomNodePin = {
	id?: string
	name?: string
	direction: "input" | "output"
	type: string
	value?: any

}

type CustomNodeData = {
	name?: string
	description?: string
	pins: CustomNodePin[]
}

interface CustomNodeType extends NodeProps {
	data : CustomNodeData
}