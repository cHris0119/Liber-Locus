import booksList from '../../mocks/lastPostsMock.json'

import styles from './SummaryProduct.module.css'

const SummaryProduct = ({ bookId }) => {
  const books = booksList.Books
  const selectedBook = books.find(book => book.id === Number(bookId))

  return (
    <ul className={styles.summaryProductContainer}>
      <h3>Resumen de compra</h3>
      <div className={styles.summaryProductDetail}>
        <li>{selectedBook.name}</li>
        <li>{selectedBook.price} CLP</li>
      </div>
      <div className={styles.summaryProductSeller}>
        <li>Vendedor: Juan lopez</li>
      </div>
    </ul>
  )
}

export default SummaryProduct
