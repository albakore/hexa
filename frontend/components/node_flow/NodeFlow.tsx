'use client'
import { useState, useCallback, CSSProperties, useId } from 'react';
import React from 'react';
import { ReactFlow, applyNodeChanges, applyEdgeChanges, addEdge, Controls, MiniMap, Background, Node, Position, Handle } from '@xyflow/react';
import '@xyflow/react/dist/base.css';
// import './flow.css'
import { Box, HStack, Text, VStack } from "@chakra-ui/react";
import { NodeProps } from '@xyflow/react';

// const initialNodes : Node[] = [
// 	{ id: 'n1', position: { x: 0, y: 0 }, data: { label: 'Node 1' } },
// 	{ id: 'n2', position: { x: 0, y: 100 }, data: { label: 'Node 2' } },
// 	{ id: 'l1', type:'chakra', position: { x: 100, y: 0 }, data: { label: 'Vector Map' } },
// 	{ id: 'l2', type:'chakra', position: { x: 100, y: 100 }, data: { label: 'Node 3' } },
// 	{ id: 'l3', type:'chakra', position: { x: 300, y: 100 }, data: { label: 'Node 4' } },
// 	{ id: 'l4', type:'chakra', position: { x: 400, y: 100 }, data: { label: 'Node 5' } },
// ];
const initialNodes : Node[] = [
	{ id: 'l1', type:'chakra', position: { x: 0, y: 0 }, data: { label: 'Node 3' } },
	{ id: 'l2', type:'chakra', position: { x: 0, y: 100 }, data: { label: 'Node 4' } },
	{ id: 'l3', type:'chakra', position: { x: 0, y: 200 }, data: { label: 'Node 5' } },
	{ id: 'l4', type:'chakra', position: { x: 0, y: 300 }, data: { label: 'Node 5' } },
];
const initialEdges = [
	{ id: 'n1-n2', source: 'n1', target: 'n2' },
	// { id: 'l1-l2', source: 'l1-fuo', target: 'l2-fua' },
	
];

function MyHandler({ type, name, label }) {


	const type_id = type == 'source' ? 'output' : 'input'
	const direction = type == 'source' ? 'row-reverse' : 'row'
	const handler_direction = type == 'target' ? Position.Left : Position.Right
	const css: CSSProperties = {
		backgroundColor: 'darkkhaki',
		outline: '1px solid',
		outlineColor: 'darkkhaki',
		outlineOffset:'1px',
		width:'2px',
		height: '2px',
		borderRadius: '1000px'
	}
	return (
		<HStack  gap={2} w={'full'} flexDirection={direction}  alignItems={'center'} >
			<Box position={'relative'}>
				<Handle
					id={`${name}:${type_id}`}
					type={type}
					position={handler_direction}
					style={css} />
			</Box>
			<Text fontSize="0.6rem">{label}</Text>
		</HStack>
	)
}

export function CustomNode(props: NodeProps) {

	const css : CSSProperties = {
		background: 'red',
		left : 0
	}

	return (
		<Box bg={'blackAlpha.500'} rounded={'md'} border={'xs'} borderColor={'gray.900'} overflow={'hidden'} w={'200px'}>
			<Box bgGradient="to-r" gradientFrom="yellow.300/60" gradientTo="blackAlpha.500" paddingInline={'10px'}>
				<Text fontSize={'0.7rem'}>{props.data.label}</Text>
			</Box>
			<HStack paddingInline={'15px'} w={'full'} paddingBlock={'3px'} alignItems={'start'}>
				<VStack w={'50%'}>
					<MyHandler
						type={'target'}
						name={'valor'}
						label={'valor'} />
					
				</VStack>
				<VStack w={'50%'}>

				<MyHandler type={'source'} name={'salida'} label={'salida'}/>
				<MyHandler type={'source'} name={'salida2'} label={'salida'}/>
				<MyHandler type={'source'} name={'salida3'} label={'output'}/>
				</VStack>
			</HStack>
    </Box>
  );
}

const nodeTypes = {
  chakra: CustomNode,
};

export default function NodeFlow() {
	const [nodes, setNodes] = useState(initialNodes);
	const [edges, setEdges] = useState(initialEdges);

	const onNodesChange = useCallback(
		(changes) => setNodes((nodesSnapshot) => applyNodeChanges(changes, nodesSnapshot)),
		[],
	);
	const onEdgesChange = useCallback(
		(changes) => setEdges((edgesSnapshot) => applyEdgeChanges(changes, edgesSnapshot)),
		[],
	);
	const onConnect = useCallback(
		(params) => setEdges((edgesSnapshot) => addEdge(params, edgesSnapshot)),
		[],
	);

	return (
		<div style={{ width: '100vw', height: '100vh' }}>

			<ReactFlow
				nodes={nodes}
				edges={edges}
				nodeTypes={nodeTypes}
				onNodesChange={onNodesChange}
				onEdgesChange={onEdgesChange}
				onConnect={onConnect}
				fitView
			>
				<Controls />
				<MiniMap />
				<Background bgColor='rgb(40,40,40)' variant="lines" gap={8} size={1} lineWidth={0.1} />
			</ReactFlow>
		</div>
	);
}