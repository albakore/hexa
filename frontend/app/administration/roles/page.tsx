import { ConfigCard } from '@/components/cards/ConfigCard'
import { Field } from '@/components/ui/field'
import { Box, Button, Editable, Image, Input, VStack, IconButton, Stack, Tabs, PopoverRoot } from '@chakra-ui/react'
import { LuCheck, LuPencilLine, LuX } from "react-icons/lu"
import React from 'react'
import { Tag } from '@/components/ui/tag'
import { PopoverArrow, PopoverBody, PopoverContent, PopoverHeader, PopoverTrigger } from '@/components/ui/popover'
import { FaPlus } from 'react-icons/fa6'
import ModuleCombobox from '@/components/combobox/Combobox'

export default function page() {
  return (
    <Box>




      <ConfigCard.Root>
        <form action="">
          {/* <ConfigCard.Header>Header util</ConfigCard.Header> */}
          <ConfigCard.Body>

            <Stack gap={5} direction={{ base: 'column', md: 'row' }} w={'full'} >
              <Box>
                <ConfigCard.Title>Datos del rol</ConfigCard.Title>
                <ConfigCard.Description>
                  <p>Corrige la informacion basica del rol.</p>
                </ConfigCard.Description>
                <VStack w={'300px'}>
                  <Field label="Nombre">
                    <Input />
                  </Field>
                  <Field label="Descripcion">
                    <Input />
                  </Field>

                </VStack>
              </Box>

              <Box
                w={'full'}
              // border={'1px solid'}
              // borderColor={'bg.emphasized'}
              // rounded={'lg'}
              // p={2}
              >
                <RoleTabContent />
              </Box>
            </Stack>
          </ConfigCard.Body>
          <ConfigCard.Footer>
            Esto es un footer
            <Button size={'sm'} ml={'auto'} rounded={'md'}>Save</Button>
          </ConfigCard.Footer>
        </form>
      </ConfigCard.Root>

    </Box >
  )
}

function EditableInput(props) {
  return (
    <Editable.Root defaultValue="Click to edit" {...props}>
      <Editable.Preview />
      <Editable.Input />
      <Editable.Control>
        <Editable.EditTrigger asChild>
          <IconButton variant="ghost" size="xs">
            <LuPencilLine />
          </IconButton>
        </Editable.EditTrigger>
        <Editable.CancelTrigger asChild>
          <IconButton variant="outline" size="xs">
            <LuX />
          </IconButton>
        </Editable.CancelTrigger>
        <Editable.SubmitTrigger asChild>
          <IconButton variant="outline" size="xs">
            <LuCheck />
          </IconButton>
        </Editable.SubmitTrigger>
      </Editable.Control>
    </Editable.Root>
  )
}

function RoleTabContent() {
  return (
    <Tabs.Root defaultValue="modules" variant="plain" fitted size={'xs'}>
      <Tabs.List
        // bg="bg.muted"
        bg="transparent"
        border={'1px solid'}
        borderColor={'bg.emphasized'}
        rounded="l3"
        p="1"
      >
        <Tabs.Trigger value="modules">
          Modules
        </Tabs.Trigger>
        <Tabs.Trigger value="groups">
          Groups
        </Tabs.Trigger>
        <Tabs.Trigger value="permissions">
          Permissions
        </Tabs.Trigger>
        <Tabs.Indicator rounded="l2" bg={'gray.600/30'} />
      </Tabs.List>
      <Tabs.Content value="modules">
        <Stack direction={'row'} wrap={'wrap'}>
          <Tag size={'lg'} closable>Providers</Tag>
          <Tag size={'lg'} closable>Client</Tag>
          <Tag size={'lg'} closable>Finance</Tag>
          <Tag size={'lg'} closable>Yiqi</Tag>
          <AddModule />
        </Stack>
      </Tabs.Content>
      <Tabs.Content value="groups">
        <Stack direction={'row'} wrap={'wrap'}>
          <Tag size={'lg'} closable>Administracion</Tag>
          <Tag size={'lg'} closable>Proveedores-Invoice</Tag>
          <Tag size={'lg'} closable>Direccion</Tag>
          <Tag size={'lg'} closable>Ver invoices</Tag>
          <Tag size={'lg'} closable>Administracion</Tag>
          <Tag size={'lg'} closable>Proveedores-Invoice</Tag>
          <Tag size={'lg'} closable>Direccion</Tag>
          <Tag size={'lg'} closable>Ver invoices</Tag>
          <Tag size={'lg'} closable>Administracion</Tag>
          <Tag size={'lg'} closable>Proveedores-Invoice</Tag>
          <Tag size={'lg'} closable>Direccion</Tag>
          <Tag size={'lg'} closable>Ver invoices</Tag>
          <Tag size={'lg'} closable>Administracion</Tag>
          <Tag size={'lg'} closable>Proveedores-Invoice</Tag>
          <Tag size={'lg'} closable>Direccion</Tag>
          <Tag size={'lg'} closable>Ver invoices</Tag>
        </Stack>
      </Tabs.Content>
      <Tabs.Content value="permissions">
        3
      </Tabs.Content>
    </Tabs.Root>
  )
}

const modules = [
  {
    id: 1,
    name: "Provider"
  },
  {
    id: 2,
    name: "Client"
  },
  {
    id: 3,
    name: "Finance"
  },
  {
    id: 4,
    name: "Yiqi"
  },
]


function AddModule() {
  // const [open, setOpen] = React.useState(false)
  return (
    <PopoverRoot positioning={{ placement: "bottom-end" }}>
      <PopoverTrigger asChild>
        <Tag size={'lg'} colorPalette={'green'} cursor={'button'}><FaPlus /></Tag>
      </PopoverTrigger>
      <PopoverContent>
        {/* <PopoverArrow /> */}
        {/* <PopoverHeader>Add Module</PopoverHeader> */}
        <PopoverBody>
          <ModuleCombobox items={modules} label={'Add Module'} labelEmpty={'No Modules found'} />
        </PopoverBody>
      </PopoverContent>
    </PopoverRoot>
  )
}