'use client'
import { Box, Button, Link as ChakraLink, Input, InputGroup, ScrollArea, Stack, Text, useToken, VStack } from '@chakra-ui/react'
import React from 'react'
import { GiMaterialsScience } from 'react-icons/gi'
import { LuExternalLink, LuSearch } from 'react-icons/lu'
import { sidebar_mock } from './sidebar-mock'
import Link from 'next/link'
import { useSelectedLayoutSegment } from 'next/navigation'

export default function SideNavScroll(props) {
	const segment = useSelectedLayoutSegment()
	const ChildType = props?.childType ?? SideNavSection
	const token = useToken('colors','bg.emphatized')

	const items = props.navlist.map((item, key) => {
		return <ChildType {...item} key={key} />
	})
	return (
		<VStack gap={2} align={'stretch'} position={'sticky'} top={14}>
			<InputGroup startElement={<LuSearch />} mb={2}>
				<Input rounded={'lg'} placeholder="Busca cualquier rol..." />
			</InputGroup>
			 <VStack align={'stretch'} w={'auto'} h={'calc(100svh - 350px)'} overflowY={'auto'} scrollBehavior={'smooth'} scrollbarWidth={'thin'} scrollbarColor={`var(${token}) transparent`} >
						{items}
					</VStack>
		</VStack>
	)
}