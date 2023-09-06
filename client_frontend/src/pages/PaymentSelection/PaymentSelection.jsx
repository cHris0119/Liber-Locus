import './PaymentSelection.css'
import BackButton from '../../components/BackButton/BackButton'
import { NavLink, useParams } from 'react-router-dom'
import SummaryProduct from '../../components/SummaryProduct/SummaryProduct'
import SelectPayment from '../../components/SelectPayment/SelectPayment'

export const PaymentSelection = () => {
  const { postId } = useParams()
  return (
    <div className='mainContent shippingDetail-container'>
      <BackButton />

      <div className='shipping-direction-container'>
        <SelectPayment />
        <div className="pagar-btn-container">
          <NavLink to={`/seleccionPago/${postId}`}>
            <button className='pagar-btn'>
              Pagar
            </button>
          </NavLink>

        </div>
      </div>

      <SummaryProduct bookId={postId} />

    </div>
  )
}
