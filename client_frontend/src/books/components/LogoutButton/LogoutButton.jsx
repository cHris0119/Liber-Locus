import { useNavigate } from 'react-router-dom'
import { FiLogOut } from 'react-icons/fi'

import styles from './LogoutButton.module.css'
import { useContext } from 'react'
import { AuthContext } from '../../../auth/context/AuthContext'

export const LogoutButton = () => {
  //
  const navigate = useNavigate()
  const { logout } = useContext(AuthContext)

  const handleLogout = () => {
    logout()
    navigate('/login', {
      replace: true
    })
  }

  return (
    <li className={styles.navbarLi}>

      <button
        className={styles.logoutButton}
        onClick={handleLogout}
      >

        <div className={styles.svg}>
          <FiLogOut />
        </div>
        <span>Salir</span>

      </button>

    </li>
  )
}
