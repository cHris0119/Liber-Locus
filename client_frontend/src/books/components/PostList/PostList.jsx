import { ProductCard } from '../'
import booksLists from '../../mocks/lastPostsMock.json'

import styles from './PostList.module.css'

export const PostList = () => {
  const posts = booksLists.Books
  const hasPost = posts.length > 0
  return (
    <>
      {hasPost
        ? (<div className={styles.postListContainer}>
          <ProductCard books={posts} />
        </div>)
        : (<h2>Cargando...</h2>)

      }
    </>
  )
}
