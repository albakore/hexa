import { RootModule } from '@/components/header/components/ModuleSelector'
import { Header } from '@/components/header/Header'
import SubHeader from '@/components/header/SubHeader'
import UserLogged from '@/components/header/UserLogged'
import { ColorModeButton } from '@/components/ui/color-mode'
import { Badge, Button, ButtonGroup, HStack, IconButton, Spacer, Text } from '@chakra-ui/react'
import React from 'react'
import { FaPlus } from 'react-icons/fa6'
import { IoIosNotificationsOutline } from 'react-icons/io'

export default function page(props) {
	const base = '/portal'
	return (
		<>
			<HeaderComponent />
			{/* <SubHeader tablist={subheader_mock} rootPath={base} /> */}
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
						{/* <Text color={'gray.600'}>/</Text>
						<Button size={'sm'} rounded={'full'} variant={'ghost'}>
							<Text>My account</Text>
						</Button> */}
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