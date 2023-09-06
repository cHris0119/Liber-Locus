import './SummaryProduct.css'
import booksList from '../../mocks/lastPostsMock.json'

const SummaryProduct = ({ bookId }) => {
  const books = booksList.Books
  const selectedBook = books.find(book => book.id === Number(bookId))

  return (
    <ul className='summaryProduct-container'>
      <h3>Resumen de compra</h3>
      <div className="summaryProduct-detail">
        <li>{selectedBook.name}</li>
        <li>{selectedBook.price} CLP</li>
      </div>
      <div className="summaryProduct-seller">
        <li>Vendedor: Juan lopez</li>
      </div>
    </ul>
  )
}

export default SummaryProduct
