import { Box, Button, ButtonGroup, Container, Heading, HStack, Spacer, Stack, Text } from '@chakra-ui/react'
import React from 'react'

function Root(props) {
	return (
		<Box
			borderBottom={'1px solid'}
			borderColor={'bg.emphasized'}
			mb={5}
		>
			<Container maxW="8xl" >

				<Stack
					alignItems={'start'}
					marginBlock={"40px"}
					wrap={'wrap'}
					gap={5}
					direction={{base:'column',sm:'column',md:'row'}}
					separator={<Spacer borderColor={'transparent'}
					/>}>
					{props.children}
				</Stack>
			</Container>
		</Box>
	)
}

function Header(props) {
	return (
		<Box >
			<Heading fontSize="3xl" fontWeight={500} mb={4}>{props.children}</Heading>
			<Text fontSize={'sm'} color={'gray.400'}>{props?.description}</Text>
		</Box>
	)
}

function Actions(props) {
	return (
		<Box >
			{props.children}
		</Box>
	)
}

export const Hero = {
	Root,
	Header,
	Actions
}
