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
                <img className='cardImg' src='https://prodimage.images-bn.com/pimages/9781435159570_p0_v1_s1200x630.jpg' alt={book.name} />
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
