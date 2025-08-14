'use client'
import DataTable from 'datatables.net-react';
import { DataTableProps } from 'datatables.net-react';
import DataTablesCore from 'datatables.net-dt';
import './chakradatatable.css'

DataTable.use(DataTablesCore);

export default function ChakraDatatable(props: DataTableProps) {
	return (
		<DataTable {...props}>
			
		</DataTable>
	)
}