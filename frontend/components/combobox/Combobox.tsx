'use client'

import {
	Badge,
	Combobox,
	Portal,
	Wrap,
	createListCollection,
} from "@chakra-ui/react"
import { useMemo, useState } from "react"

const skills = [
	"JavaScript",
	"TypeScript",
	"React",
	"Node.js",
	"GraphQL",
	"PostgreSQL",
]

export default function ModuleCombobox(props) {
	const [searchValue, setSearchValue] = useState("")
	const [selectedSkills, setSelectedSkills] = useState<Any>([])

	const filteredItems = useMemo(
		() =>
			props.items.filter((item) =>
				item.name.toLowerCase().includes(searchValue.toLowerCase()),
			),
		[searchValue],
	)

	const collection = useMemo(
		() => createListCollection({ items: filteredItems}),
		[filteredItems],
	)

	
	const handleValueChange = (details: Combobox.ValueChangeDetails) => {
		// console.log(details)
		setSelectedSkills(details.value)
	}
	console.log(filteredItems)

	return (
		<Combobox.Root
			multiple
			closeOnSelect
			positioning={{ strategy: "fixed", hideWhenDetached: true }}
			width="auto"
			value={selectedSkills}
			collection={collection}
			onValueChange={handleValueChange}
			onInputValueChange={(details) => setSearchValue(details.inputValue)}
		>
			<Wrap gap="2">
				{selectedSkills.map((item) => {
					
					return (
						<Badge key={item.id}>
							{item}
						</Badge>
				)
				})}
			</Wrap>

			<Combobox.Label>{props.label}</Combobox.Label>

			<Combobox.Control>
				<Combobox.Input />
				<Combobox.IndicatorGroup>
					<Combobox.Trigger />
				</Combobox.IndicatorGroup>
			</Combobox.Control>

			
				<Combobox.Positioner>
					<Combobox.Content>
						<Combobox.ItemGroup>
							<Combobox.ItemGroupLabel>Modules</Combobox.ItemGroupLabel>
							{filteredItems.map((item) => (
								<Combobox.Item key={item.id} item={item.name}>
									{item.name}
									<Combobox.ItemIndicator />
								</Combobox.Item>
							))}
							<Combobox.Empty>{props.labelEmpty}</Combobox.Empty>
						</Combobox.ItemGroup>
					</Combobox.Content>
				</Combobox.Positioner>
		
		</Combobox.Root>
	)
}
