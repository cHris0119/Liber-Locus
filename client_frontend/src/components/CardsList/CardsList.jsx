import './CardsList.css'
import cardsMock from '../../mocks/cardsMocks.json'
import { NavLink } from 'react-router-dom'

const CardsList = () => {
  const cards = cardsMock.Cards
  return (
    <>
      {cards.map((card) => (
        <article key={card.id} className="card-container">
          <div className='cardDetails'>
            <input type="radio" name='tarjeta'/>
            <label htmlFor="tarjeta" >
              {card.name} {card.Number}
            </label>
          </div>

          <div className='card-actions'>
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

export default CardsList
