import HomeSection from '../HomeSection/HomeSection'
import './LastPosts.css'
import lastPostBooks from '../../mocks/lastPostsMock.json'
import ProductCard from '../ProductCard/ProductCard'

const LastPosts = () => {
  const lastPost = lastPostBooks.Books

  return (
    <HomeSection>
      <div className="flex-container">
        <h2>Últimas publicaciones</h2>
        <div className="lastPost-container">
          <ProductCard books={lastPost} />
        </div>

      </div>
    </HomeSection>
  )
}

export default LastPosts
