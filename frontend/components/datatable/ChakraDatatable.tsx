'use client'
import dynamic from 'next/dynamic';
// import DataTable from 'datatables.net-react';
// import DataTablesCore from 'datatables.net-dt';
import { DataTableProps } from 'datatables.net-react';
import './chakradatatable.css'

const DataTable = dynamic(
  async () => {
    const dtReact = import('datatables.net-react');
    const dtNet = import(`datatables.net-dt`);

    const [reactMod, dtNetMod] = await Promise.all([dtReact, dtNet]);

    reactMod.default.use(dtNetMod.default);
    return reactMod.default;
  },
  { ssr: false }
);


export default function ChakraDatatable(props: DataTableProps) {
	return (
		<DataTable {...props}>
			{props.children}
		</DataTable>
	)
}