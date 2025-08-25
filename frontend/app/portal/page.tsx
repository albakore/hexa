import { RootModule } from '@/components/header/components/ModuleSelector'
import { Header } from '@/components/header/Header'
import SubHeader from '@/components/header/SubHeader'
import UserLogged from '@/components/header/UserLogged'
import { Avatar } from '@/components/ui/avatar'
import { ColorModeButton } from '@/components/ui/color-mode'
import { Badge, Box, Button, ButtonGroup, Container, GridItem, HStack, IconButton, SimpleGrid, Spacer, Stack, StackSeparator, Text } from '@chakra-ui/react'
import React from 'react'
import { FaPlus } from 'react-icons/fa6'
import { IoIosNotificationsOutline } from 'react-icons/io'
import { SlOptions } from 'react-icons/sl'

export default function page(props) {
	const base = '/portal'
	return (
		<>
			<HeaderComponent />
			{/* <SubHeader tablist={subheader_mock} rootPath={base} /> */}
			<PageLayout />
			{/* {props.children} */}
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

function PageLayout() {
	return (
		<Container maxW="8xl">
			{/* <ChakraDatatable data={data} columns={columns} className="stripe"/> */}
			<SimpleGrid columns={{ base: 2, md: 6 }} gap={{ base: "24px", md: "40px" }}>
				<GridItem colSpan={{ base: 1, md: 2 }}>
					<Text fontSize={'sm'}>Modules</Text>
				</GridItem>
				<GridItem colSpan={{ base: 1, md: 4 }} w={'full'}>
					<Text fontSize={'sm'}>Entities</Text>
					<Box>
						<ItemListRoot>
							<Item>
								<Stack direction={'row'} w={'full'} justifyContent={'space-between'} alignItems={'center'}>
									<Stack direction={'row'} gap={3} width={"calc(25% + 60px)"}>
										<Box>
											<Avatar colorPalette={'green'} />
										</Box>
										<Box>
											<Text>Mailamericas Global</Text>
											<Text fontSize={'sm'} color={'gray'}>Argentina</Text>
										</Box>
									</Stack>
									<Box>
										<Text>Nueva factura</Text>
										<Text fontSize={'sm'} color={'gray'}>por fulano@gmail.com</Text>
									</Box>
									<Box>
										<IconButton variant={'ghost'} size={'sm'}>
											<SlOptions />
										</IconButton>
									</Box>
								</Stack>
							</Item>
							<Item>
								<Stack direction={'row'} w={'full'} justifyContent={'space-between'} alignItems={'center'}>
									<Stack direction={'row'} gap={3} width={"calc(25% + 60px)"}>
										<Box>
											<Avatar colorPalette={'yellow'} />
										</Box>
										<Box>
											<Text>Proships</Text>
											<Text fontSize={'sm'} color={'gray'}>Colombia</Text>
										</Box>
									</Stack>
									<Box>
										<Text>Nueva factura</Text>
										<Text fontSize={'sm'} color={'gray'}>por fulano@gmail.com</Text>
									</Box>
									<Box>
										<IconButton variant={'ghost'} size={'sm'}>
											<SlOptions />
										</IconButton>
									</Box>
								</Stack>
							</Item>
							<Item>
								<Stack direction={'row'} w={'full'} justifyContent={'space-between'} alignItems={'center'}>
									<Stack direction={'row'} gap={3} width={"calc(25% + 60px)"}>
										<Box>
											<Avatar colorPalette={'blue'} />
										</Box>
										<Box>
											<Text>Cheyenne</Text>
											<Text fontSize={'sm'} color={'gray'}>Republica Dominicana</Text>
										</Box>
									</Stack>
									<Box>
										<Text>Nueva factura</Text>
										<Text fontSize={'sm'} color={'gray'}>por fulano@gmail.com</Text>
									</Box>
									<Box>
										<IconButton variant={'ghost'} size={'sm'}>
											<SlOptions />
										</IconButton>
									</Box>
								</Stack>
							</Item>
							<Item>
								<Stack direction={'row'} w={'full'} justifyContent={'space-between'} alignItems={'center'}>
									<Stack
										direction={'row'}
										gap={3}
										width={"calc(25% + 130px)"}


									>
										<Box>
											<Avatar colorPalette={'green'} />
										</Box>
										<Box
											width={'inherit'}
											
										>
											<Text
											textOverflow={'ellipsis'}
												whiteSpace={'nowrap'}
												overflow={'hidden'}
											>Mailamericas Global</Text>
											<Text
												fontSize={'sm'}
												color={'gray'}
												textOverflow={'ellipsis'}
												whiteSpace={'nowrap'}
												overflow={'hidden'}
											

											>Argentina el mejor pais do mondo la concha de tu madre</Text>
										</Box>
									</Stack>
									<Box>
										<Text>Nueva factura</Text>
										<Text
											fontSize={'sm'}
											color={'gray'}
										>
											por fulano@gmail.com
										</Text>
									</Box>
									<Box>
										<IconButton variant={'ghost'} size={'sm'}>
											<SlOptions />
										</IconButton>
									</Box>
								</Stack>
							</Item>

						</ItemListRoot>
					</Box>
				</GridItem>
			</SimpleGrid>

		</Container>
	)
}

function ItemListRoot(props) {
	return (
		<Stack
			border={'1px solid'}
			borderColor={'bg.emphasized'}
			rounded={'lg'}
			bg={'bg.subtle/60'}
			separator={<StackSeparator />}
			justifyContent={'center'}
			gap={0}
			{...props}
		>
			{props.children}
		</Stack>
	)
}

function Item(props) {
	return (
		<Stack p={4} {...props}>
			{props.children}
		</Stack>
	)
}