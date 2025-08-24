'use client'
import { Box, Button, Link as ChakraLink, Text, VStack } from '@chakra-ui/react'
import React from 'react'
import { GiMaterialsScience } from 'react-icons/gi'
import { LuExternalLink } from 'react-icons/lu'
import { sidebar_mock } from './sidebar-mock'
import Link from 'next/link'
import { useSelectedLayoutSegment } from 'next/navigation'

export default function SideNav(props) {
	const segment = useSelectedLayoutSegment()
	console.log(segment)
	const links = Object.groupBy(props?.navlist, ({ section }) => section)

	let items: React.JSX.Element[] = []
	Object.keys(links).forEach((key) => {
		if (key !== 'null') {
			items.push(
				<SideNavSection key={items.length}>{key.toUpperCase()}</SideNavSection>
			)
		}
		links[key]?.forEach((navlink) => {
			
			items.push(
				<SideNavLink
					{...navlink}
					key={items.length}
					route={`${props?.rootPath}${navlink.route}`}
					active={navlink?.route == `${segment ? `/${segment}`: ""}`}
				/>
			)
		})
	})
	return (
		<Box display={'flow'} position={'sticky'} top={14}>
			{items}
		</Box>
	)
}

function SideNavSection(props) {
	return (
		<Text fontSize="sm" color="gray" fontWeight={300} mt={4}>{props.children}</Text>
	)
}

function SideNavLink(props) {
	return (
		<Link href={props?.route ?? "#"} >
			<Button
				variant={props?.active ? "solid" : "ghost"}
				color={!props?.active && 'bg.inverted/80'}
				w={'full'}
				justifyContent={'start'}
				fontWeight={400}
			>
				{props?.icon}
				{props?.label}
				{props.external && <LuExternalLink w={'xs'} />}
			</Button>
		</Link>
	)
}