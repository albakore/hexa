import { ConfigCard } from '@/components/cards/ConfigCard'
import { Box, Button, Image, Input } from '@chakra-ui/react'
import React from 'react'

export default function page() {
  return (
    <Box>




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
  )
}
