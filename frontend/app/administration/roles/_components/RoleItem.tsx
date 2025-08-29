'use client'
import { Card, Text } from '@chakra-ui/react'
import Link from 'next/link'
import React from 'react'

export default function RoleItem(props) {
  return (
    <Link href={props?.id ? `/administration/roles/${props?.id}` : "#"}>
      <Card.Root p={3} w={'auto'} whiteSpace={'nowrap'} minW={'30px'}>
        <Card.Header p={0} fontSize={'sm'} fontWeight={600}>
          <Text overflow={'hidden'} textOverflow={'ellipsis'}>
            {props?.name}
          </Text>
        </Card.Header>
        <Card.Body p={0} color={'gray'} fontSize={'sm'}>
          <Text overflow={'hidden'} textOverflow={'ellipsis'}>
            {props?.description}
          </Text>
        </Card.Body>
        {/* <Card.Footer></Card.Footer> */}
      </Card.Root>
    </Link>
  )
}
