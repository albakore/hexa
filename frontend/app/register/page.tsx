import React from 'react'
import { Rbac, Users, System, CreatePermissionData, Options } from '@/backend/client'
import { Box, Button, Card, Center, Field, Input, Text, VStack } from '@chakra-ui/react'
import { PasswordInput, PasswordStrengthMeter } from '@/components/ui/password-input'

export default async function page() {

  return (
    <RegisterView/>
  )
}

function RegisterView() {

  return (
    <Center h={'100vh'}>
    <RegisterForm/>
    </Center>
  )
}



function RegisterForm() {
  return (
    <Card.Root w={'400px'}>
      <Card.Header>
        <Card.Title textAlign={'center'}>Register</Card.Title>
      </Card.Header>

      <Card.Body>
        <VStack as={'form'} gap={3}  >
        <Field.Root>
          <Field.Label>Nickname</Field.Label>
          <Input placeholder="test_user" />
        </Field.Root>

        <Field.Root>
          <Field.Label>Email or nickname</Field.Label>
          <Input placeholder="me@example.com" />
        </Field.Root>

        <Field.Root>
          <Field.Label>Name</Field.Label>
          <Input placeholder="Foo" />
        </Field.Root>

        <Field.Root>
          <Field.Label>Lastname</Field.Label>
          <Input placeholder="Bar" />
        </Field.Root>

        <Field.Root>
          <Field.Label>Password</Field.Label>
          <PasswordInput/>
          <PasswordStrengthMeter value={2} w={'full'}/>
        </Field.Root>

        <Button size={'sm'} w={'full'}>Submit</Button>

      </VStack>
      </Card.Body>

    </Card.Root>
  )
}

