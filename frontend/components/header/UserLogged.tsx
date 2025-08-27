import { Box, Button, IconButton, Link, Popover, Separator, Spacer, Stack } from '@chakra-ui/react'
import React from 'react'
import { Avatar } from '../ui/avatar'
import { FiLogOut } from 'react-icons/fi'
import MLALogo from '../logos/mailamericas'

export default function UserLogged() {
	return (
		<PopoverUserLogged />
	)
}

function UserLoggedButton() {
	return (
		<IconButton size="sm" asChild rounded={'full'} variant={'outline'}>
			<Avatar size={'sm'} colorPalette={'green'}/>
		</IconButton>
	)
}


function PopoverUserLogged() {
	return (
		<Popover.Root positioning={{ placement: "bottom-end" }}>
			<Popover.Trigger>
				<UserLoggedButton />
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
							<Box paddingInline={4} pt={2}>
								<Popover.Title>Kevin Kener</Popover.Title>
								<Popover.Title color={'gray'}>kkener@mailamericas.com</Popover.Title>
							</Box>

							<LinkAsButton href="/portal">Dashboard</LinkAsButton>
							<LinkAsButton href="/account/settings">Account Settings</LinkAsButton>
						</Stack>
						<Separator />
						<Stack p={2} gap={1}>
							<LinkAsButton href="/administration">Administration</LinkAsButton>
							{/* <LinkAsButton>Create Invoice</LinkAsButton> */}
							<LinkAsButton>Theme</LinkAsButton>
						</Stack>
						<Separator />
						<Stack p={2} gap={1}>
							<LinkAsButton href="/" colorPalette="red">Home Page <Spacer /><MLALogo/> </LinkAsButton>
							<LinkAsButton href="/login">Log Out <Spacer /><FiLogOut/> </LinkAsButton>
						</Stack>
					</Popover.Body>
				</Popover.Content>
			</Popover.Positioner>
		</Popover.Root>
	)
}


function LinkAsButton(props) {
	return (
		<Button asChild variant={'ghost'} justifyContent={'start'} size={'sm'} color={{base:"bg.inverted/70", _hover:"bg.inverted"}}>
			<Link href={props.href ?? "#"} justifyContent={'space-between'}>{props.children}</Link>
		</Button>
	)
}