import { Box, Button, Link, Text, VStack } from '@chakra-ui/react'
import React from 'react'
import { GiMaterialsScience } from 'react-icons/gi'
import { LuExternalLink } from 'react-icons/lu'

export default function Sidebar() {
	return (
		<Box display={'flow'}>
			<SectionTarget icon={<GiMaterialsScience />} label="Overview" />
			<SectionTarget icon={<GiMaterialsScience />} label="Notebooks" />
			<Section>COMPUTE</Section>
			<SectionTarget icon={<GiMaterialsScience />} label="Vercel Functions" />
			<SectionTarget active icon={<GiMaterialsScience />} label="External APIs" />
			<SectionTarget icon={<GiMaterialsScience />} label="Middleware" />
			<Section>EDGE NETWORK</Section>
			<SectionTarget icon={<GiMaterialsScience />} label="Edge Requests" />
			<SectionTarget icon={<GiMaterialsScience />} label="Fast Data Transfer" />
			<SectionTarget icon={<GiMaterialsScience />} label="Image Optimization" />
			<Section>EXTERNALS</Section>
			<SectionTarget external icon={<GiMaterialsScience />} label="Vercel Functions" />
			<SectionTarget external icon={<GiMaterialsScience />} label="External APIs" />
		</Box>
	)
}

function Section(props) {
	return (
		<Text fontSize="sm" color="gray" fontWeight={300} mt={4}>{props.children}</Text>
	)
}

function SectionTarget(props) {
	return (
		<Button
			asChild
			variant={props?.active ? "solid" : "ghost"}
			color={!props?.active && 'bg.inverted/80'}
			w={'full'}
			justifyContent={'start'}
			fontWeight={400}
		>
			<Link href={props?.href ?? "#"}>
				{props?.icon}
				{props?.label}
				{props.external && <LuExternalLink w={'xs'}/>}
			</Link>
		</Button>
	)
}