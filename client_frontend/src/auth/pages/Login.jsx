import { Link, useNavigate } from 'react-router-dom'
import { Input, Button } from '../components/'

import styles from '../styles/Login.module.css'
import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'

export const Login = ({ setLoggedIn }) => {
  const navigate = useNavigate()
  const { login } = useContext(AuthContext)

  const handleSubmit = (event) => {
    event.preventDefault()
    login('Chris')
    navigate('/home', {
      replace: true
    })
  }

  return (
    <div className={styles.authPage}>
      <div className={styles.formContainer}>
        <form className={styles.form} onSubmit={handleSubmit}>
          <h3 className={styles.title}>Inicio de Sesión</h3>
          <Input
            placeholder="Ingresa tu correo..."
            label="Correo"
            name="email"
            type="email"
          />

          <Input
            placeholder="Ingresa tu contraseña..."
            label="Contraseña"
            name="password"
            type="password"
          />
          <Button
            backgroundColor="#c75200"
            buttonText="Iniciar Sesión"
          />
          <span className={styles.link}>
          Aun no tienes cuenta? <Link to="/auth/registro">Registrate</Link>
          </span>
          <span className={styles.link}>
           <Link to="/auth/recuperarContra">Olvidaste tu contraseña?</Link>
          </span>
        </form>
      </div>
      <div className={styles.backgroundDark}>

      </div>
    </div>

  )
}
