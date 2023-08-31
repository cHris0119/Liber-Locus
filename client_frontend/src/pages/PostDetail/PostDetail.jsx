import { useParams } from 'react-router-dom'
import booksList from '../../mocks/lastPostsMock.json'
import './PostDetail.css'

const PostDetail = () => {
  const books = booksList.Books
  const { postId } = useParams()

  const selectedBook = books.find(book => book.id === Number(postId))

  return (
    <div className='productDetail-container'>
      <div className="productDetails">

        <div className="productImg-container">
          <img className='productImg' src="" alt={selectedBook.name} />
        </div>
        <div className="productInfo">
          <ul className='productInfo-names'>
            <li>{selectedBook.name}</li>
            <li>{selectedBook.category}</li>
            <li>{selectedBook.price} CLP</li>
            <li>Vendedor: Juan</li>
          </ul>
          <button className='buyButton'>Comprar</button>
        </div>
        <div className="description">
        </div>

      </div>

      <p >Lorem ipsum, dolor sit amet consectetur adipisicing elit. Necessitatibus repellendus, quis cum optio enim impedit earum modi ea alias! Optio nam alias iure repellendus mollitia sapiente voluptatem perspiciatis vitae minus.</p>

    </div>
  )
}

export default PostDetail
