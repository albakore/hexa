import React from 'react'

export default function page(props) {
	const {params} = props
	const {uuid} = params
  return (
	  <div>page {uuid}</div>
  )
}
