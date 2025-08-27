import { RootModule } from '@/components/header/components/ModuleSelector'
import { Header } from '@/components/header/Header'
import SubHeader from '@/components/header/SubHeader'
import UserLogged from '@/components/header/UserLogged'
import { ColorModeButton } from '@/components/ui/color-mode'
import { Badge, Button, ButtonGroup, HStack, IconButton, Link, Spacer, Text } from '@chakra-ui/react'
import React from 'react'
import { FaPlus } from 'react-icons/fa6'
import { IoIosNotificationsOutline } from 'react-icons/io'
import { LuFolder, LuSquareCheck, LuUser } from 'react-icons/lu'

const subheader_mock = [
	{
		label: "Overview",
		value: "overview",
		route: "",
		icon: <LuSquareCheck />
	},
	{
		label: "Users",
		value: "users",
		route: "/users",
		icon: <LuUser />
	},
	{
		label: "Roles",
		value: "roles",
		route: "/roles",
		icon: <LuFolder />
	},
	{
		label: "Modules",
		value: "modules",
		route: "/modules",
		icon: <LuFolder />
	},
	{
		label: "System",
		value: "system",
		route: "/system",
		// icon: <LuSquareCheck />
	},
]


export default function layout(props) {
	const base = '/administration'
	return (
		<>
			<HeaderComponent />
			<SubHeader tablist={subheader_mock} rootPath={base} />
			{props.children}
		</>
	)
}

function HeaderComponent() {
	return (
		<Header.Root >
			<Header.Logo />
			<Header.Body>
				<HStack>
					<Button size={'sm'} rounded={'full'} variant={'ghost'}>
						<Text>Kevin Kener <Badge colorPalette={'green'} size={'sm'} rounded={'full'}>Administrator</Badge></Text>
					</Button>
					<RootModule>
						<Text color={'gray.600'}>/</Text>
						<Button size={'sm'} rounded={'full'} variant={'ghost'}>
							<Text>Administration</Text>
						</Button>
					</RootModule>

				</HStack>
			</Header.Body>
			<Spacer />
			<Header.Actions>
				<HStack
					gap={4}
				>
					<ButtonGroup variant={'outline'} size={'sm'}>
						<IconButton rounded={'full'}><FaPlus /></IconButton>
						<IconButton rounded={'full'}><IoIosNotificationsOutline /></IconButton>
						<ColorModeButton rounded={'full'} />
						{/* <Button asChild rounded={'full'}>
							<Link href="/login">
								Iniciar Sesion
							</Link>
						</Button> */}
					</ButtonGroup>
					<UserLogged />
				</HStack>
			</Header.Actions>
		</Header.Root>
	)
}