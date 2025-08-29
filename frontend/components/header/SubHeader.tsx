'use client'
import { Box, Container, For, Link as ChakraLink, Tabs } from '@chakra-ui/react'
import { usePathname, useRouter, useSelectedLayoutSegment } from 'next/navigation'
import React from 'react'
import { LuFolder, LuSquareCheck, LuUser } from 'react-icons/lu'
import Link from 'next/link'


const subheader_mock = [
	{
		label: "Overview",
		value: "overview",
		route: "",
		icon: <LuUser />
	},
	{
		label: "Integrations",
		value: "integrations",
		route: "/integrations",
		icon: <LuFolder />
	},
	{
		label: "Deployments",
		value: "deployments",
		route: "/deployments",
		icon: <LuSquareCheck />
	},
	{
		label: "Activity",
		value: "activity",
		route: "/activity",
		icon: null
	},
	{
		label: "Settings",
		value: "settings",
		route: "/settings",
		icon: null
	}
]

export default function SubHeader(props) {
	const segment = useSelectedLayoutSegment()
	return (
		<Root active={segment ?? props?.tablist[0].value} >
			<For each={props?.tablist}>
				{(tab, index) => (
					<NavTab
						key={index}
						route={`${props?.rootPath}${tab?.route}`}
						value={tab?.value}
					>
						{tab?.icon}
						{tab.label}
					</NavTab>
				)}
			</For>
		</Root>
	)
}

function Root(props) {
	return (
		<Box
			borderBottom={'1px solid'}
			borderColor={'bg.emphasized'}
			position={'sticky'} top={0}
			bg={'bg'}
			zIndex={200}
		>
			<Container
				maxW={'8xl'}
				paddingBlock={1}
			>
				<Tabs.Root
					activationMode={'automatic'}
					defaultValue={props?.active}
					variant="plain"
					size={'xs'}
					p={0}
					w={'fit'}
				>
					<Tabs.List bg="transparent" rounded="l3" padding={0} w={'fit'}>
						{props?.children}
						<Tabs.Indicator
							bg={'bg.inverted/7'}
							rounded="l2"
							css={{
								transition: "all 200ms ease",
							}}
						/>
					</Tabs.List>

				</Tabs.Root>
			</Container>
		</Box>
	)
}

function NavTab(props) {
	return (
		<Link href={props?.route ?? "#"}>
			<Tabs.Trigger  {...props}>
				{props.children}
			</Tabs.Trigger>
		</Link>
	)
}
