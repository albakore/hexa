import ChakraDatatable from "@/components/datatable/ChakraDatatable";
import { Box } from "@chakra-ui/react";

const columns = [
	{ name: "id", title: "Id" },
	{ name: "name", title: "Name" },
	{ name: "lastname", title: "Lastname" },
	{ name: "age", title: "Age" },
	{ name: "role", title: "Role" },
]


const data = [
	[1,
	"Kevin",
	"Kener",
	29,
	"Administrator"]
]
export default function page() {
	return (
		<Box w={'full'}>
			<ChakraDatatable data={data} columns={columns} className="stripe" />
		</Box>
	)
}