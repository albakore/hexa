import { HStack, IconButton, Input, InputGroup, Popover, Portal, RadioCardItem, RadioCardItemIndicator, RadioCardLabel, RadioCardRoot, StackSeparator, VStack } from "@chakra-ui/react"
import { CgArrowsExchangeAltV } from "react-icons/cg"
import { FaCheck } from "react-icons/fa6"
import { FiPackage } from "react-icons/fi"
import { LuSearch } from "react-icons/lu"

export function RootModule(props) {
	return (
		<HStack>
			{props.children}
			<ModuleSelector />
		</HStack>
	)
}


export function ModuleSelector() {
	return (
		<Popover.Root positioning={{ placement: "bottom-start" }}>
			<Popover.Trigger asChild>
				<IconButton size="md" variant="ghost" m={0} p={0} minW={'20px'}>
					<CgArrowsExchangeAltV scale={'40px'} />
				</IconButton>
			</Popover.Trigger>
			<Portal>
				<Popover.Positioner >
					<Popover.Content rounded={"2xl"} minW={'600px'}>
						<Popover.Body p={0} w={'full'}>
							{/* <Popover.Title fontWeight="medium">Naruto Form</Popover.Title> */}
							<HStack
								gap={0}
								separator={
									<StackSeparator />}
							>
								<ModuleMenu />
								<ModuleMenu />
							</HStack>
							{/* <Input placeholder="Your fav. character" size="sm" /> */}
						</Popover.Body>
					</Popover.Content>
				</Popover.Positioner>
			</Portal>
		</Popover.Root>
	)
}

export function ModuleMenu() {
	return (
		<VStack w={'full'}>
			<InputGroup flex="1" startElement={<LuSearch />}>
				<Input placeholder="Search modules" variant={'flushed'} />
			</InputGroup>

			<VStack w={'full'} alignItems={'stretch'}>
				<RadioCardRoot
					p={2}
					orientation={'horizontal'}
					align="start"
					justify="start"
					variant={'subtle'}
					gap={0}
				>
					<RadioCardLabel paddingInline={3} paddingBlock={2} color={'gray.400'} fontWeight={300}>Modules</RadioCardLabel>
					<ModuleItem icon={FiPackage} value="provider">Provider</ModuleItem>
					<ModuleItem icon={FiPackage} value="client">Client</ModuleItem>
					<ModuleItem icon={FiPackage} value="invoicing">Invoicing</ModuleItem>
					<ModuleItem icon={FiPackage} value="finance">Finance</ModuleItem>
				</RadioCardRoot>
			</VStack>
		</VStack>
	)
}

export function ModuleItem(props) {
	return (

		<RadioCardItem
			value={props.value}
			flexDirection={'row'}
			gap={3}
			shadowColor={'none'}
			bg={'none'}
			_hover={{ bg: "bg.muted" }}
			indicator={<RadioCardItemIndicator checked={<FaCheck />} rounded={'none'} border={0}></RadioCardItemIndicator>}
			icon={<props.icon size={'20px'} />}
			label={props.children}
			p={3}
		/>
	)
}

