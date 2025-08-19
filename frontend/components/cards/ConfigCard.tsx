import { Box, Heading, Stack, Text } from '@chakra-ui/react'
import React from 'react'

function Root(props) {
	return (
		<Box
			border={'1px solid'}
			borderColor={`bg.emphasized`}
			rounded={'lg'}
			{...props}
		>
			{props?.children}
		</Box>
	)
}

function Title(props) {
	return (
		<Heading fontSize={'2xl'}>
			{props?.children}
		</Heading>
	)
}

function Description(props) {
	return (
		<Text fontSize={'sm'} marginBlock={4}>
			{props?.children}
		</Text>
	)
}

function Header(props) {
	return (
		<Box
			as={'header'}
			paddingBlock={4}
			paddingInline={6}
			borderBottom={'1px solid'}
			borderColor={'bg.emphasized'}
			{...props}
		>
			{props?.children}
		</Box>
	)
}

function Body(props) {
	return (
		<Box
			p={6}
			{...props}
		>
			{props?.children}
		</Box>
	)
}

function Footer(props) {
	return (
		<Stack
			as={'footer'}
			paddingBlock={4}
			paddingInline={6}
			borderTop={'1px solid'}
			borderColor={'bg.emphasized'}
			direction={'row'}
			alignItems={'center'}
			{...props}
		>
			{props?.children}
		</Stack>
	)
}

export const ConfigCard = {
	Root,
	Header,
	Title,
	Description,
	Body,
	Footer,
}