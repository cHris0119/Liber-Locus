import { useContext } from 'react'
import { NavBar } from '..'
import { linksModal } from '../../services/linksArray'

import styles from './AccountButton.module.css'
import { AuthContext } from '../../../auth/context/AuthContext'

export const AccountButton = ({ NavOpen, modalOpen, handleModal }) => {
  const { authState } = useContext(AuthContext)
  const { user } = authState
  return (

    <div
    onClick={() => handleModal()}
    className={styles['Account-container']}
    >

      <div className={styles.Account}>
        <div className={styles['Account-img']}></div>
        {NavOpen
          ? (<p className={styles.Username}>{user?.name}</p>)
          : undefined
        }
      </div>

      {modalOpen
        ? (
          <div className={styles.Modal}>
            <NavBar
              links={linksModal}
              NavOpen={true}
              style='navbarModal'
              modal={true}
            />
          </div>
          )
        : undefined}

    </div>
  )
}
