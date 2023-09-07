import { useParams, NavLink } from 'react-router-dom'
import SelectDirection from '../components/SelectDirection/SelectDirection'
import BackButton from '../components/BackButton/BackButton'
import SummaryProduct from '../components/SummaryProduct/SummaryProduct'

import styles from '../styles/ShippingDetail.module.css'

const ShippingDetail = () => {
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

export default ShippingDetail
