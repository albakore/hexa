'use client'

import {
	Badge,
	Button,
	Combobox,
	Portal,
	Stack,
	Wrap,
	createListCollection,
} from "@chakra-ui/react"
import { useMemo, useState } from "react"
import { Tag } from "../ui/tag"

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
	const [selectedItems, setSelectedItems] = useState<Any>([])

	const filteredItems = useMemo(
		() =>
			props.items.filter((item) =>
				item.name.toLowerCase().includes(searchValue.toLowerCase()),
			),
		[searchValue],
	)

	const collection = useMemo(
		() => createListCollection({ items: filteredItems }),
		[filteredItems],
	)

	const selectedObjects = useMemo(
		() => props.items.filter((item) => selectedItems.some((value) => value === item.name)),
		[selectedItems],
	)

	const handleValueChange = (details: Combobox.ValueChangeDetails) => {
		setSelectedItems(details.value)
	}

	const handleDeleteItem = (data) => {
		setSelectedItems(selectedItems.filter(item => item !== data))
	}

	const handleSubmitSelected = async () => {
		await setTimeout(() => {
			console.log(selectedObjects)
			setSelectedItems([])
		}, 1000);
	}

	return (
		<Combobox.Root
			multiple
			closeOnSelect
			size={'sm'}
			
			positioning={{ strategy: "fixed", hideWhenDetached: true }}
			width="auto"
			value={selectedItems}
			collection={collection}
			onValueChange={handleValueChange}
			onInputValueChange={(details) => setSearchValue(details.inputValue)}
		>

			<Combobox.Label>{props.label}</Combobox.Label>

			<Stack direction={'row'} w={'full'}>
				<Combobox.Control>
				<Combobox.Input rounded={'lg'}/>
				<Combobox.IndicatorGroup>
					<Combobox.Trigger />
				</Combobox.IndicatorGroup>
				</Combobox.Control>
				
				<Button size={'sm'} rounded={'lg'} disabled={!selectedItems.length} onClick={handleSubmitSelected}>Save</Button>
			</Stack>


			<Combobox.Positioner>
				<Combobox.Content>
					<Combobox.ItemGroup>
						<Combobox.ItemGroupLabel>Modules</Combobox.ItemGroupLabel>
						{filteredItems.map((item, key) => (
							<Combobox.Item key={key} item={item.name}>
								{item.name}
								<Combobox.ItemIndicator />
							</Combobox.Item>
						))}
						<Combobox.Empty>{props.labelEmpty}</Combobox.Empty>
					</Combobox.ItemGroup>
				</Combobox.Content>
			</Combobox.Positioner>

			<Wrap gap="2">
				{selectedItems.map((item, key) => {

					return (
						<Tag key={key} closable onClose={() => handleDeleteItem(item)}>
							{item}
						</Tag>
					)
				})}
			</Wrap>


		</Combobox.Root>
	)
}
