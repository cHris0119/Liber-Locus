import NavBar from '../NavBar/NavBar'
import { linksModal } from '../../services/linksArray'

import styles from './AccountButton.module.css'

const AccountButton = ({ NavOpen, modalOpen, handleModal }) => {
  return (
    <div onClick={() => handleModal()} className={styles['Account-container']}>
      <div className={styles.Account}>
        <div className={styles['Account-img']}></div>
        {NavOpen ? <p className={styles.Username}>Nombre usuario</p> : undefined}
      </div>
      {modalOpen
        ? (
          <div className={styles.Modal}>
            <NavBar links={linksModal} NavOpen={true} style='Navbar-modal' />
          </div>
        )
        : undefined}
    </div>
  )
}

export default AccountButton
