import './MarketplaceHeader.css'
import Filters from '../Filters/Filters'
import Searcher from '../Searcher/Searcher'

const MarketplaceHeader = () => {
  return (
    <div className='market-header'>
      <Filters />
      <Searcher />
      <button className='publishBook'>Publicar</button>
    </div>
  )
}

export default MarketplaceHeader
