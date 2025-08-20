'use client'
import { Box, Container, For, Link, Tabs } from '@chakra-ui/react'
import { usePathname, useRouter } from 'next/navigation'
import React from 'react'
import { LuFolder, LuSquareCheck, LuUser } from 'react-icons/lu'


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

export default function SubHeader() {
	const pathname = usePathname()
	return (
		<Root>
			<For each={subheader_mock}>
				{(tab, index) => (
					<NavTab
						key={index}
						route={`${pathname}${tab?.route}`}
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
					defaultValue="members"
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
		<Tabs.Trigger  asChild {...props} >
			<Link unstyled
				href={props?.route ?? "#"}
				>
				{props.children}
			</Link>
		</Tabs.Trigger>
	)
}
