import { ConfigCard } from '@/components/cards/ConfigCard'
import { Hero } from '@/components/hero/Hero'
import SideNav from '@/components/sidenav/SideNav'
import { Box, Button, ButtonGroup, Container, GridItem, HStack, Image, Input, SimpleGrid } from '@chakra-ui/react'
import React from 'react'

const sidenav_links = [
  {
    label: "Personal Information",
    route: "",
    section: null,
    icon: null,
    active: false,
    external: false,
  },
  {
    label: "Security",
    route: "/security",
    section: null,
    icon: null,
    active: false,
  }
]

export default function page() {
  
  const rootPath = '/administration'

  return (
    <>
      <HeroPage />
      <BodyPage>
        {/* <SimpleGrid columns={{ base: 2, md: 5 }} gap={{ base: "24px", md: "40px" }} position={'relative'}>
          <GridItem position={'relative'}>
            <SideNav navlist={sidenav_links} rootPath={rootPath} />
          </GridItem>
          <GridItem colSpan={{ base: 1, md: 4 }}>
            {props?.children}
          </GridItem>
          </SimpleGrid> */}
      </BodyPage>
    </>
  )
}


function HeroPage() {
  return (
    <Hero.Root>
      <Hero.Header description="Este es el inicio del administrador">
        Administration Overview
      </Hero.Header>
      {/* <Hero.Actions>
        <ButtonGroup variant="outline">
          <Button>Action</Button>
          <Button>Action</Button>
          <Button>Action</Button>
        </ButtonGroup>
      </Hero.Actions> */}
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

