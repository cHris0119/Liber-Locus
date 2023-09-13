import { NavLink } from 'react-router-dom'
import { CardsList } from '../'

import styles from './SelectPayment.module.css'

export const SelectPayment = () => {
  return (

    <div className={styles.selectPaymentContainer}>

      <div className={styles.cardPayContainer}>
        <h2>Selecciona tu tarjeta</h2>

        <div className={styles.cardPaymentMain}>l
          <CardsList />
        </div>

        <footer className={styles.cardFooter}>
          <NavLink className={styles.linkEditCard}>Agregar nueva tarjeta</NavLink>
        </footer>

      </div>

    </div>
  )
}
