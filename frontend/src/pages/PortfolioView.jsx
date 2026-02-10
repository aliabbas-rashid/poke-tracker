import React, {useEffect, useState} from 'react'
import {getPortfolio, createItem, getPortfolioValue} from '../lib/api'
import ItemCard from '../components/ItemCard'

export default function PortfolioView({portfolioId}){
  const [portfolio, setPortfolio] = useState(null)
  const [items, setItems] = useState([])
  const [name, setName] = useState('')
  const [price, setPrice] = useState('')
  const [value, setValue] = useState(null)

  useEffect(()=>{fetchData()}, [portfolioId])
  async function fetchData(){
    const p = await getPortfolio(portfolioId)
    setPortfolio(p)
    setItems(p.items || [])
    const v = await getPortfolioValue(portfolioId)
    setValue(v)
  }

  async function onAdd(e){
    e.preventDefault()
    if(!name || !price) return
    await createItem(portfolioId, {name, purchase_price_gbp: parseFloat(price)})
    setName(''); setPrice('')
    fetchData()
  }

  if(!portfolio) return <div>Loading...</div>

  return (
    <div>
      <h2>{portfolio.name}</h2>
      <p>{portfolio.description}</p>
      <div>
        <form onSubmit={onAdd}>
          <input placeholder="Item name" value={name} onChange={e=>setName(e.target.value)} />
          <input placeholder="Purchase price (GBP)" value={price} onChange={e=>setPrice(e.target.value)} />
          <button type="submit">Add Item</button>
        </form>
      </div>
      <h3>Items</h3>
      <div>
        {items.map(it => <ItemCard key={it.id} item={it} />)}
      </div>
      <h3>Portfolio Value</h3>
      {value && <div>Total purchase: £{value.total_purchase_gbp} | Current: £{value.total_current_gbp} | Change: {value.change_pct?.toFixed(2)}%</div>}
    </div>
  )
}

