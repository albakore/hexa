import { ConfigCard } from "@/components/cards/ConfigCard";
import ChakraDatatable from "@/components/datatable/ChakraDatatable";
import { Header } from "@/components/header/Header";
import UserLogged from "@/components/header/UserLogged";
import HeroSection, { Hero } from "@/components/hero/Hero";
import Sidebar from "@/components/sidebar/Sidebar";
import { CheckboxCard } from "@/components/ui/checkbox-card";
import { ColorModeButton } from "@/components/ui/color-mode";
import { RadioCardItem, RadioCardItemIndicator, RadioCardLabel, RadioCardRoot } from "@/components/ui/radio-card";
import { Badge, Box, Button, ButtonGroup, Container, GridItem, HStack, IconButton, Input, InputGroup, Kbd, Link, Popover, Portal, Separator, SimpleGrid, Spacer, StackSeparator, Text, VStack } from "@chakra-ui/react";
import { ConfigColumns } from "datatables.net-dt";
import { CgArrowsExchangeAltV, CgArrowsV } from "react-icons/cg";
import { FaCheck, FaPlus } from "react-icons/fa6";
import { FiPackage } from "react-icons/fi";
import { IoIosNotificationsOutline } from "react-icons/io";
import { LuSearch } from "react-icons/lu";

const columns: ConfigColumns[] = [
	{ name: "id", title: "Id" },
	{ name: "name", title: "Name" },
	{ name: "lastname", title: "Lastname" },
	{ name: "age", title: "Age" },
	{ name: "role", title: "Role" },

]


const data = [
	[1,
		"Kevin",
		"Kener",
		29,
		"Administrator"]
]
export default function page() {
	return (
		<Box w={'full'}>
			<HeaderComponent />
			<Hero.Root>
				<Hero.Header description="Esta es una descripcion detallada de como se ve una descripcion en el hero">
					Overview
				</Hero.Header>
				<Hero.Actions>
					<ButtonGroup variant="outline">
						<Button>Action</Button>
						<Button>Action</Button>
						<Button>Action</Button>
					</ButtonGroup>
				</Hero.Actions>
			</Hero.Root>
			<Container maxW="8xl">
				{/* <ChakraDatatable data={data} columns={columns} className="stripe"/> */}
				<SimpleGrid columns={{ base: 2, md: 5 }} gap={{ base: "24px", md: "40px" }}>
					<GridItem>
						<Sidebar />
					</GridItem>
					<GridItem colSpan={{ base: 1, md: 4 }}>
						<Box>
							<ConfigCard.Root>
								<form action="">
								<ConfigCard.Header>Header util</ConfigCard.Header>
								<ConfigCard.Body>
									<ConfigCard.Title>User</ConfigCard.Title>
									<ConfigCard.Description>Configuracion de usuario</ConfigCard.Description>

									<Input/>

								</ConfigCard.Body>
								<ConfigCard.Footer>
										Esto es un footer
										<Button size={'sm'} ml={'auto'} rounded={'md'}>Save</Button>
									</ConfigCard.Footer>
									</form>
							</ConfigCard.Root>
						</Box>
					</GridItem>
				</SimpleGrid>
				<HStack>


				</HStack>
			</Container>
		</Box>
	)
}

function HeaderComponent() {
	return (
		<Header.Root>
			<Header.Logo />
			<Header.Body>
				<Button size={'sm'} rounded={'full'} variant={'ghost'}>
					<Text>Kevin Kener <Badge colorPalette={'green'} size={'sm'} rounded={'full'}>Administrator</Badge></Text>
				</Button>
				<RootModule>
					<Text color={'gray.600'}>/</Text>
					<Button size={'sm'} rounded={'full'} variant={'ghost'}>
						<Text>Providers</Text>
					</Button>
				</RootModule>
				<RootModule>
					<Text color={'gray.600'}>/</Text>
					<Button size={'sm'} rounded={'full'} variant={'ghost'}>
						<Text>Mailamericas</Text>
					</Button>
				</RootModule>
				{/* <HStack
						as={'nav'}
						gap={4}
					>
						<Link>Inicio</Link>
						<Link>Facturas</Link>
						<Link>Carga masiva</Link>
						<Link>Acerca de</Link>
					</HStack> */}
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
						<Button asChild rounded={'full'}>
							<Link href="/login">
								Iniciar Sesion
							</Link>
						</Button>
					</ButtonGroup>
					<UserLogged />
				</HStack>
			</Header.Actions>
		</Header.Root>
	)
}

function RootModule(props) {
	return (
		<HStack>
			{props.children}
			<ModuleSelector />
		</HStack>
	)
}


function ModuleSelector() {
	return (
		<Popover.Root positioning={{ placement: "bottom-start" }}>
			<Popover.Trigger asChild>
				<IconButton size="md" variant="ghost" m={0} p={0} minW={'20px'}>
					<CgArrowsExchangeAltV scale={'40px'} />
				</IconButton>
			</Popover.Trigger>
			<Portal>
				<Popover.Positioner >
					<Popover.Content rounded={"2xl"} minW={'600px'}>
						<Popover.Body p={0} w={'full'}>
							{/* <Popover.Title fontWeight="medium">Naruto Form</Popover.Title> */}
							<HStack
								gap={0}
								separator={
									<StackSeparator />}
							>
								<ModuleMenu />
								<ModuleMenu />
							</HStack>
							{/* <Input placeholder="Your fav. character" size="sm" /> */}
						</Popover.Body>
					</Popover.Content>
				</Popover.Positioner>
			</Portal>
		</Popover.Root>
	)
}

function ModuleMenu() {
	return (
		<VStack w={'full'}>
			<InputGroup flex="1" startElement={<LuSearch />}>
				<Input placeholder="Search modules" variant={'flushed'} />
			</InputGroup>

			<VStack w={'full'} alignItems={'stretch'}>
				<RadioCardRoot
					p={2}
					orientation={'horizontal'}
					align="start"
					justify="start"
					variant={'subtle'}
					gap={0}
				>
					<RadioCardLabel paddingInline={3} paddingBlock={2} color={'gray.400'} fontWeight={300}>Modules</RadioCardLabel>
					<ModuleItem icon={FiPackage} value="provider">Provider</ModuleItem>
					<ModuleItem icon={FiPackage} value="client">Client</ModuleItem>
					<ModuleItem icon={FiPackage} value="invoicing">Invoicing</ModuleItem>
					<ModuleItem icon={FiPackage} value="finance">Finance</ModuleItem>
				</RadioCardRoot>
			</VStack>
		</VStack>
	)
}

function ModuleItem(props) {
	return (

		<RadioCardItem
			value={props.value}
			flexDirection={'row'}
			gap={3}
			shadowColor={'none'}
			bg={'none'}
			_hover={{ bg: "bg.muted" }}
			indicator={<RadioCardItemIndicator checked={<FaCheck />} rounded={'none'} border={0}></RadioCardItemIndicator>}
			icon={<props.icon size={'20px'} />}
			label={props.children}
			p={3}
		/>
	)
}

