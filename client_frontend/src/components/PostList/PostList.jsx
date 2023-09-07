import ProductCard from '../ProductCard/ProductCard'
import booksLists from '../../mocks/lastPostsMock.json'

import styles from './PostList.module.css'

const PostList = () => {
  const posts = booksLists.Books
  const hasPost = posts.length > 0

  console.log(posts)
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

export default PostList
