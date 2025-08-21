import { ConfigCard } from "@/components/cards/ConfigCard";
import ChakraDatatable from "@/components/datatable/ChakraDatatable";
import { RootModule } from "@/components/header/components/ModuleSelector";
import { Header } from "@/components/header/Header";
import SubHeader from "@/components/header/SubHeader";
import UserLogged from "@/components/header/UserLogged";
import { Hero } from "@/components/hero/Hero";
import Sidebar from "@/components/sidenav/SideNav";
import { CheckboxCard } from "@/components/ui/checkbox-card";
import { ColorModeButton } from "@/components/ui/color-mode";
import { RadioCardItem, RadioCardItemIndicator, RadioCardLabel, RadioCardRoot } from "@/components/ui/radio-card";
import { Badge, Box, Button, ButtonGroup, Container, GridItem, HStack, IconButton, Image, Input, InputGroup, Kbd, Link, Popover, Portal, Separator, SimpleGrid, Spacer, StackSeparator, Tabs, Text, VStack } from "@chakra-ui/react";
import { ConfigColumns } from "datatables.net-dt";
import { CgArrowsExchangeAltV, CgArrowsV } from "react-icons/cg";
import { FaCheck, FaPlus } from "react-icons/fa6";
import { FiPackage } from "react-icons/fi";
import { IoIosNotificationsOutline } from "react-icons/io";
import { LuFolder, LuSearch, LuSquareCheck, LuUser } from "react-icons/lu";

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
		<Box w={'full'} >
			<HeaderComponent />

			<SubHeader tablist={subheader_mock} />


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
									{/* <ConfigCard.Header>Header util</ConfigCard.Header> */}
									<ConfigCard.Body>
										<Image src="https://picsum.photos/200/200?random=1" rounded={'full'} float={'right'} w={'100px'} mb={4} />
										<ConfigCard.Title>Avatar</ConfigCard.Title>
										<ConfigCard.Description>
											<p>Configuracion de avatar.</p>
											<p>Selecciona la imagen que quieras cargar.</p>
										</ConfigCard.Description>
										{/* <Input /> */}
									</ConfigCard.Body>
									<ConfigCard.Footer>
										Esto es un footer
										<Button size={'sm'} ml={'auto'} rounded={'md'}>Save</Button>
									</ConfigCard.Footer>
								</form>
							</ConfigCard.Root>


							<ConfigCard.Root>
								<form action="">
									{/* <ConfigCard.Header>Header util</ConfigCard.Header> */}
									<ConfigCard.Body>
										<ConfigCard.Title>Email</ConfigCard.Title>
										<ConfigCard.Description>
											<p>Configuracion de email.</p>
										</ConfigCard.Description>
										<Input />
									</ConfigCard.Body>
									<ConfigCard.Footer>
										Esto es un footer
										<Button size={'sm'} ml={'auto'} rounded={'md'}>Save</Button>
									</ConfigCard.Footer>
								</form>
							</ConfigCard.Root>

							<ConfigCard.Root>
								<form action="">
									{/* <ConfigCard.Header>Header util</ConfigCard.Header> */}
									<ConfigCard.Body>
										<ConfigCard.Title>Nickname</ConfigCard.Title>
										<ConfigCard.Description>
											<p>Configuracion del nickname.</p>
										</ConfigCard.Description>
										{/* <Input /> */}
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
							<Text>Providers</Text>
						</Button>
					</RootModule>
					<RootModule>
						<Text color={'gray.600'}>/</Text>
						<Button size={'sm'} rounded={'full'} variant={'ghost'}>
							<Text>Mailamericas</Text>
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
