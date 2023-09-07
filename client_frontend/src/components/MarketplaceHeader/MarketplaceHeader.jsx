import Filters from '../Filters/Filters'
import Searcher from '../Searcher/Searcher'
import { NavLink } from 'react-router-dom'

import styles from './MarketplaceHeader.module.css'

const MarketplaceHeader = () => {
  return (
    <div className={styles.marketHeader}>
      <Filters />
      <Searcher />
      <NavLink className={styles.publishBook} to={'/publicarLibro'}>
        <button className={styles.publishBookButton}>Publicar</button>
      </NavLink>
    </div>
  )
}

export default MarketplaceHeader
