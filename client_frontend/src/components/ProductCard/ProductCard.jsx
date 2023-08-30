import './ProductCard.css'
const ProductCard = ({ books }) => {
  return (
    <>
      {books.map((book) => (
        <article key={book.id} className='lastPost-Card'>
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
      ))}
    </>
  )
}

export default ProductCard
