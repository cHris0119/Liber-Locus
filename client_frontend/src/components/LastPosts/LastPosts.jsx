import HomeSection from '../HomeSection/HomeSection'
import lastPostBooks from '../../mocks/lastPostsMock.json'
import ProductCard from '../ProductCard/ProductCard'

import styles from './LastPosts.module.css'

const LastPosts = () => {
  const lastPost = lastPostBooks.Books.slice(0, 4)

  return (
    <HomeSection>
      <div className={styles.flexContainer}>
        <h2>Últimas publicaciones</h2>
        <div className={styles.lastPostContainer}>
          <ProductCard books={lastPost} />
        </div>

      </div>
    </HomeSection>
  )
}

export default LastPosts
