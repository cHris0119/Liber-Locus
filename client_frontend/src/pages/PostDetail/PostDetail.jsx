import { useParams } from 'react-router-dom'
import booksList from '../../mocks/lastPostsMock.json'
import './PostDetail.css'
import BackButton from '../../components/BackButton/BackButton'
import QuestionsPost from '../../components/QuestionsPost/QuestionsPost'

const PostDetail = () => {
  const books = booksList.Books
  const { postId } = useParams()

  const selectedBook = books.find(book => book.id === Number(postId))

  return (
    <>
      <div className='productDetail-container'>
        <BackButton />
        <div className="productImg-container">
          <img className='productImg' src="https://prodimage.images-bn.com/pimages/9781435159570_p0_v1_s1200x630.jpg" alt={selectedBook.name} />
        </div>
        <div className="productInfo">
          <ul className='productInfo-names'>
            <li className='productCategory'>{selectedBook.category}</li>
            <li className='productName'>{selectedBook.name}</li>
            <li className='productPrice'>{selectedBook.price} CLP</li>
            <li className='productSeller'>Vendedor: Juan</li>
            <li className='productDescription'><p>Buen libro, buena historia, bla bla bla.</p></li>
          </ul>
          <div className="buyButton-container">
            <button className='buyButton'>Comprar</button>
          </div>
        </div>
      </div>

      <QuestionsPost />
    </>
  )
}

export default PostDetail
