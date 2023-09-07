import BackButton from '../components/BackButton/BackButton'
import { NavLink, useParams } from 'react-router-dom'
import SummaryProduct from '../components/SummaryProduct/SummaryProduct'
import SelectPayment from '../components/SelectPayment/SelectPayment'

import styles from '../styles/PaymentSelection.module.css'

const PaymentSelection = () => {
  const { postId } = useParams()
  return (
    <div className={styles.paymentDetailContainer}>
      <BackButton />

      <div className={styles.paymentContainer}>
        <SelectPayment />
        <div className={styles.pagarBtnContainer}>
          <NavLink to={`/seleccionPago/${postId}`}>
            <button className={styles.pagarBtn}>
              Pagar
            </button>
          </NavLink>

        </div>
      </div>

      <SummaryProduct bookId={postId} />

    </div>
  )
}

export default PaymentSelection
