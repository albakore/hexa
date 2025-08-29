'use client'
import { Box, Button, ClientOnly, CloseButton, Dialog, Portal } from "@chakra-ui/react"
import React from 'react'
import { useRouter } from "next/navigation"

export default function UserModal(props) {
	// const { params } = await props
	// const { uuid } = await params
	const router = useRouter()
	return (
		<Dialog.Root defaultOpen onExitComplete={()=>router.back()}>
			{/* <Dialog.Trigger asChild>
		  <Button variant="outline" size="sm">
			Open Dialog
		  </Button>
		</Dialog.Trigger> */}
		<Portal>
			<Dialog.Backdrop />
			<Dialog.Positioner>
				<Dialog.Content>
					<Dialog.Header>
						{/* <Dialog.Title>User {uuid}</Dialog.Title> */}
					</Dialog.Header>
					<Dialog.Body>
						<p>
							Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do
							eiusmod tempor incididunt ut labore et dolore magna aliqua.
						</p>
					</Dialog.Body>
					<Dialog.Footer>
						<Dialog.ActionTrigger asChild>
							<Button variant="outline">Cancel</Button>
						</Dialog.ActionTrigger>
						<Button>Save</Button>
					</Dialog.Footer>
					<Dialog.CloseTrigger asChild>
						<CloseButton size="sm" />
					</Dialog.CloseTrigger>
				</Dialog.Content>
			</Dialog.Positioner>
		</Portal>
		</Dialog.Root>
		// <dialog open style={{zIndex: 300}}>
		// 	<p>Greetings, one and all!</p>
		// </dialog>
	)
}