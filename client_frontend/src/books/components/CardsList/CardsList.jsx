import cardsMock from '../../mocks/cardsMocks.json'
import { NavLink } from 'react-router-dom'

import styles from './CardsList.module.css'

export const CardsList = () => {
  const cards = cardsMock.Cards
  return (
    <>
      {cards.map((card) => (
        <article key={card.id} className={styles.cardContainer}>
          <div className={styles.cardDetails}>
            <input type="radio" name='tarjeta'/>
            <label htmlFor="tarjeta" >
              {card.name} {card.Number}
            </label>
          </div>

          <div className={styles.cardActions}>
            <button>
              <NavLink>Editar</NavLink>
            </button>
            <button>Eliminar</button>
          </div>

        </article>
      ))}
    </>
  )
}
