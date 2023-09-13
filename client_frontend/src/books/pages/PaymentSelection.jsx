import { NavLink, useParams } from 'react-router-dom'
import { BackButton, SummaryProduct, SelectPayment } from '../components/'

import styles from '../styles/PaymentSelection.module.css'

export const PaymentSelection = () => {
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
