import React, {useEffect, useState} from 'react'
import {getItemPrice, refreshItemPrice, getItemHistory} from '../lib/api'

export default function ItemCard({item}){
  const [price, setPrice] = useState(null)
  const [history, setHistory] = useState([])

  useEffect(()=>{fetchPrice()}, [])
  async function fetchPrice(){
    const p = await getItemPrice(item.id)
    setPrice(p)
    const h = await getItemHistory(item.id)
    setHistory(h || [])
  }
  async function onRefresh(){
    await refreshItemPrice(item.id)
    fetchPrice()
  }
  return (
    <div style={{border:'1px solid #ddd', padding:10, marginBottom:10}}>
      <strong>{item.name}</strong>
      <div>Purchase: £{item.purchase_price_gbp}</div>
      <div>Current: {price?.price_gbp ? `£${price.price_gbp} (${price.source})` : 'N/A'}</div>
      <div><button onClick={onRefresh}>Refresh price</button></div>
    </div>
  )
}

