import './MarketplaceHeader.css'
import Filters from '../Filters/Filters'
import Searcher from '../Searcher/Searcher'
import { NavLink } from 'react-router-dom'

const MarketplaceHeader = () => {
  return (
    <div className='market-header'>
      <Filters />
      <Searcher />
      <NavLink className='publishBook' to={'/publicarLibro'}>
        <button className='publishBook-button'>Publicar</button>
      </NavLink>
    </div>
  )
}

export default MarketplaceHeader
