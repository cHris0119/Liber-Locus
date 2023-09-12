import { Input, Button } from '../components'
import { Link } from 'react-router-dom'
import styles from '../styles/Login.module.css'

export const RecuperarContra = () => {
  const handleSubmit = (e) => {
    e.preventDefault()
  }
  return (
    <div className={styles.authPage}>
    <div className={styles.formContainer}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <h3 className={styles.title}>Recuperar contraseña</h3>
        <Input
            placeholder="Ingresa tu correo..."
            label="Correo"
            name="email"
            type="email"
          />

        <Button
          backgroundColor="#c75200"
          buttonText="Enviar correo"

        />
        <span className={styles.link}>
          Ya tienes cuenta? <Link to="/auth/login">Inicia Sesión</Link>
        </span>
      </form>
    </div>
    <div className={styles.backgroundDark}>

    </div>
  </div>
  )
}
