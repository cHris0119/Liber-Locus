import { NavLink } from 'react-router-dom'
import styles from './ProductCard.module.css'

export const ProductCard = ({ books }) => {
  return (
    <>
      {books.map((book) => (
        <NavLink to={`/detallePost/${book.id}`} key={book.id} className={styles.customNavlink}>
          <article className={styles.lastPostCard}>

            <div className={styles.cardInfo}>

              <div className={styles.cardImgContainer}>
                <img className={styles.cardImg} src='https://prodimage.images-bn.com/pimages/9781435159570_p0_v1_s1200x630.jpg' alt={book.name} />
              </div>

              <div className={styles.cardDetails}>
                <div>
                  <h3>{book.name}</h3>
                </div>

                <div className={styles.cardDescription}>
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
