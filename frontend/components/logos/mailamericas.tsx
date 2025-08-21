"use client"
import React from 'react'
import { useColorModeValue } from '../ui/color-mode'
import { useToken } from '@chakra-ui/react'


export default function MLALogo() {
	const token = useToken('colors', 'fg')
	return (
		<svg width="460" height="460" viewBox="0 0 460 460" fill="none" xmlns="http://www.w3.org/2000/svg">
			<path d="M460 380V0L380 80V460L460 380Z" fill={token[0]} />
			<path d="M330 380V130.5L250 210.5V460L330 380Z" fill={token[0]} />
			<path fillRule="evenodd" clipRule="evenodd" d="M80 0L0 80H379.726L459.726 0H80Z" fill="#76BD1D" />
			<path fillRule="evenodd" clipRule="evenodd" d="M80 132L0 212H249.726L329.726 132H80Z" fill="#76BD1D" />
		</svg>
	)
}
