import './ProductCard.css'
import { NavLink } from 'react-router-dom'

const ProductCard = ({ books }) => {
  return (
    <>
      {books.map((book) => (
        <NavLink to={`/detallePost/${book.id}`} key={book.id} className='custom-navlink'>
          <article className='lastPost-Card'>
            <div className="card-info">
              <div className="cardImg-container">
                <img src="" alt={book.name} />
              </div>
              <div className="card-details">
                <div className="card-name">
                  <h3>{book.name}</h3>
                </div>
                <div className="card-description">
                  <p>{book.price} CLP</p>
                  <span>{book.category}</span>
                </div>
              </div>

            </div>

          </article>
        </NavLink>
      ))}
    </>
  )
}

export default ProductCard
