import booksList from '../../mocks/lastPostsMock.json'
import { useParams } from 'react-router-dom'
import SelectDirection from '../../components/SelectDirection/SelectDirection'
import './ShippingDetail.css'
import BackButton from '../../components/BackButton/BackButton'
import SummaryProduct from '../../components/SummaryProduct/SummaryProduct'

const ShippingDetail = () => {
  const { postId } = useParams()
  const books = booksList.Books
  const selectedBook = books.find(book => book.id === Number(postId))
  console.log(selectedBook)

  return (
    <div className='mainContent shippingDetail-container'>
      <BackButton />

      <div className='shipping-direction-container'>
        <SelectDirection />
        <div className="continuar-btn-container">
          <button className='continuar-btn'>Continuar</button>
        </div>
      </div>

      <SummaryProduct book={selectedBook} />

    </div>
  )
}

export default ShippingDetail
