import { Input, Button } from '../components'
import { Link, useNavigate } from 'react-router-dom'
import styles from '../styles/Login.module.css'

export const Register = () => {
  const navigate = useNavigate()
  const handleSubmit = (e) => {
    e.preventDefault()
    navigate('/auth/direccionRegistro')
  }

  return (
    <div className={styles.authPage}>
      <div className={styles.formContainer}>
        <form className={styles.form} onSubmit={handleSubmit}>
          <h3 className={styles.title}>Crea tu cuenta</h3>
          <div className={styles.twoInputs}>
            <Input
              placeholder="Nombre..."
              label="Nombre"
              name="firstname"
              type="text"
            />

            <Input
              placeholder="Apellido..."
              label="Apellido"
              name="lastname"
              type="text"
            />
          </div>
          <Input
            placeholder="Ingresa un correo..."
            label="Correo"
            name="email"
            type="email"
          />

          <Input
            placeholder="Ingresa una contraseña..."
            label="Contraseña"
            name="password"
            type="password"
          />

          <Input
            placeholder="Confirma la contraseña..."
            label="Confirmar Contraseña"
            name="confirmPassword"
            type="password"
          />
          <Button
            backgroundColor="#c75200"
            buttonText="Siguiente"

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
