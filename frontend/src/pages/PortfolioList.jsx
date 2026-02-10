import React, {useEffect, useState} from 'react'
import {listPortfolios, createPortfolio} from '../lib/api'

export default function PortfolioList({onSelect}){
  const [portfolios, setPortfolios] = useState([])
  const [name, setName] = useState('')

  useEffect(()=>{ fetchPortfolios() }, [])
  async function fetchPortfolios(){
    const res = await listPortfolios()
    setPortfolios(res || [])
  }
  async function onCreate(e){
    e.preventDefault()
    if(!name) return
    await createPortfolio({name})
    setName('')
    fetchPortfolios()
  }
  return (
    <div>
      <h2>Portfolios</h2>
      <form onSubmit={onCreate}>
        <input value={name} onChange={e=>setName(e.target.value)} placeholder="Portfolio name" />
        <button type="submit">Create</button>
      </form>
      <ul>
        {portfolios.map(p=> (
          <li key={p.id} style={{cursor:'pointer'}} onClick={()=> onSelect && onSelect(p.id)}>
            {p.name} - {p.description || ''}
          </li>
        ))}
      </ul>
    </div>
  )
}
