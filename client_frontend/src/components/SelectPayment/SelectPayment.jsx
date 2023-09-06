import CardsList from '../CardsList/CardsList'
import './SelectPayment.css'
import { NavLink } from 'react-router-dom'

const SelectPayment = () => {
  return (
    <div className='selectPayment-container'>

      <div className='cardPay-container'>
        <h2>Selecciona tu tarjeta</h2>
        <div className='cardPayment-main'>
          <CardsList />
        </div>

        <footer className="direction-footer">
          <NavLink className='link-editDirection'>Agregar nueva tarjeta</NavLink>
        </footer>
      </div>

    </div>
  )
}

export default SelectPayment
