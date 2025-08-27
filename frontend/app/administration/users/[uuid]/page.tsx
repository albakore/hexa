import React from 'react'

export default function page(props) {
	const {params} = props
  return (
	  <div>page { params.uuid}</div>
  )
}
