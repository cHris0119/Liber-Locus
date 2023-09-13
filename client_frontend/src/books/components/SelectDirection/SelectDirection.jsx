import { NavLink } from 'react-router-dom'

import styles from './SelectDirection.module.css'

export const SelectDirection = () => {
  return (

    <div className={styles.selectDirectionContainer}>

      <h2>Selecciona tu dirección</h2>

      <div className={styles.directionContainer}>

        <div className={styles.directionMain}>
          <header className={styles.directionHeader}>
            <p>Enviar a domicilio</p>
            <p>$ 3.000 <span>{'>'}</span></p>
          </header>
          <main className={styles.directionMain}>
            <p>Dirección falsa 1234</p>
          </main>
        </div>

        <footer className={styles.directionFooter}>
          <NavLink className={styles.linkEditDirection}>Editar o elegir otro domicilio</NavLink>
        </footer>

      </div>

    </div>

  )
}
