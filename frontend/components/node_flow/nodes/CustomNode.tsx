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