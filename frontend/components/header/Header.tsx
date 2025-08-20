import { Box, Container, HStack, IconButton, Image, VStack } from '@chakra-ui/react'
import React from 'react'
import MLALogo from '../logos/mailamericas'

function Root(props) {
	return (
		<Box
			as="header"
			// borderBottom={'1px solid'}
			// borderColor={'bg.emphasized'}
			bg={'bg'}
			zIndex={300}
			
		>
			<Container maxW={'8xl'} paddingBlock={3}>
				<HStack gap={8} fontSize={'sm'} alignItems={'start'}>
					{props.children}
				</HStack>
			</Container>
		</Box>
	)
}

function Logo() {
	return (
		<Box>
			<IconButton variant={'ghost'} p={2} rounded={'full'}>
				{/* <Image src={'vercel.svg'}/> */}
				<MLALogo />
			</IconButton>
		</Box>
	)
}

function Body(props) {
	return (
		<HStack>{props.children}</HStack>
	)
}

function Actions(props) {
	return (
		<HStack>{props.children}</HStack>
	)
}

export const Header = {
	Root,
	Logo,
	Body,
	Actions
}
