import { Input, Button } from '../components'
import { Link, useNavigate } from 'react-router-dom'
import styles from '../styles/Login.module.css'

export const DirectionRegister = () => {
  const navigate = useNavigate()
  const handleSubmit = (e) => {
    e.preventDefault()
    navigate('/')
  }
  return (
    <div className={styles.authPage}>
    <div className={styles.formContainer}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <h3 className={styles.title}>Direccion</h3>
        <Input
            placeholder="Comuna..."
            label="Comuna"
            name="comuna"
            type="text"
          />
        <div className={styles.twoInputs}>
          <Input
            placeholder="Calle..."
            label="Calle"
            name="Calle"
            type="text"
          />

          <Input
            placeholder="Número..."
            label="Numero"
            name="Numero"
            type="text"
          />
        </div>

        <Button
          backgroundColor="#c75200"
          buttonText="Crear Cuenta"

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
