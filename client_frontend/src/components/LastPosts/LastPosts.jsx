import HomeSection from '../HomeSection/HomeSection'
import './LastPosts.css'
import lastPostBooks from '../../mocks/lastPostsMock.json'

const LastPosts = () => {
  const lastPost = lastPostBooks.Books

  return (
    <HomeSection>
      <div className="flex-container">
        <h2>Últimas publicaciones</h2>
        <div className="lastPost-container">
          {lastPost.map((book) => (
            <article key={book.id} className='lastPost-Card'>
              <div className="card-info">
                <div className="cardImg-container">
                  <img src="" alt={book.name} />
                </div>
                <div className="card-details">
                  <div className="card-description">
                    <h3>{book.name}</h3>
                    <p>{book.price} CLP</p>
                  </div>
                  <div className="category-container">
                    <span>{book.category}</span>
                  </div>
                </div>

              </div>
              <div className="verDetalles-container">
                <span className='verDetalles'>Ver detalles</span>
              </div>

            </article>
          ))}
        </div>

      </div>
    </HomeSection>
  )
}

export default LastPosts
