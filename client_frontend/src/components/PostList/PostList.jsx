import './PostList.css'
import ProductCard from '../ProductCard/ProductCard'
import booksLists from '../../mocks/lastPostsMock.json'

const PostList = () => {
  const posts = booksLists.Books
  const hasPost = posts.length > 0

  console.log(posts)
  return (
    <>
      {hasPost
        ? (<div className="postList-container">
          <ProductCard books={posts} />
        </div>)
        : (<h2>Cargando...</h2>)

      }
    </>
  )
}

export default PostList
