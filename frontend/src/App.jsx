import React, {useState} from 'react'
import PortfolioList from './pages/PortfolioList'
import PortfolioView from './pages/PortfolioView'

export default function App(){
  const [selected, setSelected] = useState(null)
  return (
    <div style={{padding: 20}}>
      <h1>Poke Tracker</h1>
      {!selected && <PortfolioList onSelect={id => setSelected(id)} />}
      {selected && <div><button onClick={()=>setSelected(null)}>Back</button><PortfolioView portfolioId={selected} /></div>}
    </div>
  )
}
