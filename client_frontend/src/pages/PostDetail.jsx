import { useParams, NavLink } from 'react-router-dom'
import booksList from '../mocks/lastPostsMock.json'
import { BackButton, QuestionsPost } from '../components/'

import styles from '../styles/PostDetail.module.css'

export const PostDetail = () => {
  const books = booksList.Books
  const { postId } = useParams()
  const selectedBook = books.find(book => book.id === Number(postId))

  return (
    <>
      <div className={styles.productDetailContainer}>
        <BackButton />
        <div className={styles.productImgContainer}>
          <img className={styles.productImg} src="https://prodimage.images-bn.com/pimages/9781435159570_p0_v1_s1200x630.jpg" alt={selectedBook.name} />
        </div>

        {/* Este div tiene que ser un componente. */}
        <div className={styles.productInfo}>
          <ul className={styles.productInfoNames}>
            <li className={styles.productCategory}>{selectedBook.category}</li>
            <li className={styles.productName}>{selectedBook.name}</li>
            <li className={styles.productPrice}>{selectedBook.price} CLP</li>
            <li className={styles.productSeller}>Vendedor: Juan</li>
            <li className={styles.productDescription}><p>Buen libro, buena historia, bla bla bla.</p></li>
          </ul>
          <div className={styles.buyButtonContainer}>
            <NavLink className={styles.linkBuyButton} to={`/detalleEnvio/${postId}`}><button className={styles.buyButton} >Comprar</button></NavLink>
          </div>
        </div>
      </div>

      <QuestionsPost />
    </>
  )
}
