import { useParams, NavLink } from 'react-router-dom'
import { SelectDirection, BackButton, SummaryProduct } from '../components/'

import styles from '../styles/ShippingDetail.module.css'

export const ShippingDetail = () => {
  const { postId } = useParams()

  return (

    <div className={styles.shippingDetailContainer}>
      <BackButton />

      <div className={styles.shippingDirectionContainer}>
        <SelectDirection />
        <div className={styles.continuarBtnContainer}>
          <NavLink to={`/seleccionPago/${postId}`}>
            <button className={styles.continuarBtn}>
              Continuar
            </button>
          </NavLink>

        </div>
      </div>

      <SummaryProduct bookId={postId} />

    </div>
  )
}
