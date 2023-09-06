import { useParams, NavLink } from 'react-router-dom'
import SelectDirection from '../../components/SelectDirection/SelectDirection'
import './ShippingDetail.css'
import BackButton from '../../components/BackButton/BackButton'
import SummaryProduct from '../../components/SummaryProduct/SummaryProduct'

const ShippingDetail = () => {
  const { postId } = useParams()

  return (
    <div className='mainContent shippingDetail-container'>
      <BackButton />

      <div className='shipping-direction-container'>
        <SelectDirection />
        <div className="continuar-btn-container">
          <NavLink to={`/seleccionPago/${postId}`}>
            <button className='continuar-btn'>
              Continuar
            </button>
          </NavLink>

        </div>
      </div>

      <SummaryProduct bookId={postId} />

    </div>
  )
}

export default ShippingDetail
