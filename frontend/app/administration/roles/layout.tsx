import { ConfigCard } from '@/components/cards/ConfigCard'
import { Hero } from '@/components/hero/Hero'
import SideNavScroll from '@/components/sidenav-scroll/SideNavScroll'
import SideNav from '@/components/sidenav/SideNav'
import { Box, Button, ButtonGroup, Container, GridItem, HStack, Image, Input, SimpleGrid } from '@chakra-ui/react'
import React from 'react'
import RoleItem from './_components/RoleItem'

const sidenav_links = [
  {
    id: 1,
    name: "Admin",
    description: "Es el admin"
  },
  {
    id: 2,
    name: "Provider Provider Provider Provider",
    description: "Provedores de mailamericas, lorem ipsum"
  },
  {
    id: 3,
    name: "Gerente Sistemas",
    description: "Administrador del portal"
  },
  // {
  //   id: 1,
  //   name: "Admin",
  //   description: "Es el admin"
  // },
  // {
  //   id: 2,
  //   name: "Provider Provider Provider Provider",
  //   description: "Provedores de mailamericas, lorem ipsum"
  // },
  // {
  //   id: 3,
  //   name: "Gerente Sistemas",
  //   description: "Administrador del portal"
  // },
  // {
  //   id: 1,
  //   name: "Admin",
  //   description: "Es el admin"
  // },
  // {
  //   id: 2,
  //   name: "Provider Provider Provider Provider",
  //   description: "Provedores de mailamericas, lorem ipsum"
  // },
  // {
  //   id: 3,
  //   name: "Gerente Sistemas",
  //   description: "Administrador del portal"
  // },
  // {
  //   id: 1,
  //   name: "Admin",
  //   description: "Es el admin"
  // },
  // {
  //   id: 2,
  //   name: "Provider Provider Provider Provider",
  //   description: "Provedores de mailamericas, lorem ipsum"
  // },
  // {
  //   id: 3,
  //   name: "Gerente Sistemas",
  //   description: "Administrador del portal"
  // },
  // {
  //   id: 1,
  //   name: "Admin",
  //   description: "Es el admin"
  // },
  // {
  //   id: 2,
  //   name: "Provider Provider Provider Provider",
  //   description: "Provedores de mailamericas, lorem ipsum"
  // },
  // {
  //   id: 3,
  //   name: "Gerente Sistemas",
  //   description: "Administrador del portal"
  // },
]

export default function layout(props) {
  
  const rootPath = '/administration/roles'

  return (
	<>
	  <HeroPage />
	  <BodyPage>
		<SimpleGrid columns={{ base: 2, md: 5 }} gap={{ base: "24px", md: "40px" }} position={'relative'}>
		  <GridItem position={'relative'}>
			<SideNavScroll navlist={sidenav_links} rootPath={rootPath} childType={RoleItem} />
		  </GridItem>
		  <GridItem colSpan={{ base: 1, md: 4 }}>
			{props?.children}
		  </GridItem>
		  </SimpleGrid>
	  </BodyPage>
	</>
  )
}


function HeroPage() {
  return (
	<Hero.Root>
	  <Hero.Header description="Aca se encuentran todas las configuraciones de roles">
		Roles
	  </Hero.Header>
	  <Hero.Actions>
		<ButtonGroup variant="outline">
		  <Button>Nuevo rol</Button>
		  {/* <Button>Action</Button>
		  <Button>Action</Button> */}
		</ButtonGroup>
	  </Hero.Actions>
	</Hero.Root>
  )
}

function BodyPage(props) {
  return (
	<Container maxW="8xl">
	  {/* <ChakraDatatable data={data} columns={columns} className="stripe"/> */}
	  {props.children}
	</Container>
  )
}
