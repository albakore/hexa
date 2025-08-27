'use client'
import { ConfigCard } from '@/components/cards/ConfigCard'
import { Hero } from '@/components/hero/Hero'
import SideNav from '@/components/sidenav/SideNav'
import { Status } from '@/components/ui/status'
import { Badge, Box, Button, ButtonGroup, ClientOnly, Container, Flex, For, GridItem, HStack, IconButton, Image, Input, InputGroup, Link, Pagination, Popover, Separator, SimpleGrid, Spacer, Stack, StackSeparator, Text } from '@chakra-ui/react'
import React from 'react'
import { FaTrash } from 'react-icons/fa6'
import { HiChevronLeft, HiChevronRight } from 'react-icons/hi'
import { LuSearch } from 'react-icons/lu'
import { SlOptions } from 'react-icons/sl'

export default function page() {

  const rootPath = '/administration/users'

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



        <UserList />
      </BodyPage>
    </>
  )
}


function HeroPage() {
  return (
    <Hero.Root>
      <Hero.Header description="Aca se encuentran todos los usuarios">
        Users
      </Hero.Header>
      <Hero.Actions>
        <ButtonGroup variant="outline">
          <Button variant={'solid'}>Nuevo Usuario</Button>
          {/* <Button></Button> */}
          <Button>Exportar</Button>
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

const pageSize = 5
const count = 50
const items = new Array(count)
  .fill(0)
  .map((_, index) => `Lorem ipsum dolor sit amet ${index + 1}`)

function UserList() {
  const [page, setPage] = React.useState(1)

  const startRange = (page - 1) * pageSize
  const endRange = startRange + pageSize

  const visibleItems = items.slice(startRange, endRange)

  const render_items = visibleItems.map((item, index) => (
    <Stack direction='row' key={index} padding={4} justifyContent={'space-between'}>
      <Box minW={'30px'}>
        <Stack direction={'row'} whiteSpace={'nowrap'}>
          <Text lineHeight={'20px'} overflow={'hidden'} textOverflow={'ellipsis'}><b>Kevin Kener</b></Text>
          <Badge overflow={'hidden'} textOverflow={'ellipsis'}>Administrator</Badge>
        </Stack>
        <Text fontSize={'sm'} color={'gray'}>kkener</Text>
      </Box>
      <Box minW={'30px'} whiteSpace={'nowrap'}>
        <Text fontSize={'sm'} overflow={'hidden'} textOverflow={'ellipsis'} >Desarrollador de software</Text>
        <Text fontSize={'sm'} color={'gray'} overflow={'hidden'} textOverflow={'ellipsis'}>kkener@mailamericas.com</Text>
      </Box>
      <Box minW={'30px'} whiteSpace={'nowrap'}>
        <Stack direction={'row'}>
          <Status />
          <Text lineHeight={'20px'}> Activo</Text>
        </Stack>

        <Text fontSize={'sm'} color={'gray'} overflow={'hidden'} textOverflow={'ellipsis'}>desde 45/45/45</Text>
      </Box>
      <ColumnOptions />
    </Stack>
  ))

  return (
    <Stack gap={4} >
      <Stack direction={'row'}>
        <InputGroup startElement={<LuSearch />} >
          <Input rounded={'lg'} placeholder="Busca cualquier dato..." />
        </InputGroup>
        <Box>
          <SelectStatus />
        </Box>
      </Stack>
      <Stack gap={0} border={'1px solid'} borderColor={'bg.emphasized'} separator={<StackSeparator bg={'red'} />} rounded={'lg'}>
        {render_items}
      </Stack>
      <Pagination.Root
        count={count}
        pageSize={pageSize}
        page={page}
        onPageChange={(e) => setPage(e.page)}
      >
        <ButtonGroup variant="ghost" size="sm">
          <Pagination.PrevTrigger asChild>
            <IconButton>
              <HiChevronLeft />
            </IconButton>
          </Pagination.PrevTrigger>

          <Pagination.Items
            render={(page) => (
              <IconButton variant={{ base: "ghost", _selected: "outline" }}>
                {page.value}
              </IconButton>
            )}
          />

          <Pagination.NextTrigger asChild>
            <IconButton>
              <HiChevronRight />
            </IconButton>
          </Pagination.NextTrigger>
        </ButtonGroup>
      </Pagination.Root>
    </Stack>
  )
}

function UserItemColumn(props) {
  return (
    <Stack>
      {props.children}
    </Stack>
  )
}

function ColumnDataName(props) {
  return (
    <Box>
      <Text>{props.name} {props.lastname}</Text>
      <Text>{props.nickname}</Text>
    </Box>
  )
}

function ColumnOptions(props) {
  return (
    <Popover.Root positioning={{ placement: "bottom-end" }}>
      <Popover.Trigger asChild>
        <IconButton size={'sm'} variant={'ghost'}>
          <SlOptions />
        </IconButton>
      </Popover.Trigger>
      <Popover.Positioner>
        <Popover.Content
          w={'full'}
          maxW={'800px'}
          border={'1px solid'}
          borderColor={'bg.emphasized'}
          rounded={'xl'}
        >
          <Popover.CloseTrigger />

          <Popover.Body p={0}>
            <Stack p={2} gap={1}>
              <LinkAsButton href="#">Inspeccionar</LinkAsButton>
              <LinkAsButton href="#">Asignar Rol</LinkAsButton>
              <LinkAsButton href="#">Inactivar</LinkAsButton>
            </Stack>
            <Separator />
            <Stack p={2} gap={1}>
              <Button colorPalette={'red'} variant={'ghost'}>Eliminar <Spacer /><FaTrash /> </Button>
            </Stack>
          </Popover.Body>
        </Popover.Content>
      </Popover.Positioner>
    </Popover.Root>
  )
}

function LinkAsButton(props) {
  return (
    <Button asChild variant={'ghost'} justifyContent={'start'} size={'sm'} color={{ base: "bg.inverted/70", _hover: "bg.inverted" }} {...props}>
      <Link href={props.href ?? "#"} justifyContent={'space-between'}>{props.children}</Link>
    </Button>
  )
}

import { Portal, Select, createListCollection } from "@chakra-ui/react"

function SelectStatus() {
  return (
    <Select.Root collection={frameworks} >
      <Select.HiddenSelect />
      {/* <Select.Label>Select framework</Select.Label> */}
      <Select.Control w={'300px'}>
        <Select.Trigger  rounded={'lg'} >
          <Select.ValueText placeholder={
            (<Stack direction={'row'}>
              <Box>
                <Status colorPalette={'green'}/>
              <Status colorPalette={'red'}/>
              <Status colorPalette={'orange'}/>
              <Status colorPalette={'blue'} />
              </Box>
               Elige el estado
            </Stack>)
          } />
        </Select.Trigger>
        <Select.IndicatorGroup>
          <Select.Indicator />
        </Select.IndicatorGroup>
      </Select.Control>
      <Portal>
        <Select.Positioner>
          <Select.Content>
            {frameworks.items.map((framework) => (
              <Select.Item item={framework} key={framework.value}>
                <Stack direction={'row'}>
                  {framework.icon}
                  <Text lineHeight={'20px'}> {framework.label}</Text>
                </Stack>
                
                <Select.ItemIndicator />
              </Select.Item>
            ))}
          </Select.Content>
        </Select.Positioner>
      </Portal>
    </Select.Root>
  )
}

const frameworks = createListCollection({
  items: [
    { icon: <Status colorPalette={'green'}/>,label: "Activo", value: "activo" },
    { icon: <Status colorPalette={'gray'} />,label: "Inactivo", value: "inactivo" },

  ],
})