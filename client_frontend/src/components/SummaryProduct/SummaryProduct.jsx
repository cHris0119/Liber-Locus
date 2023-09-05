import './SummaryProduct.css'

const SummaryProduct = ({ book }) => {
  return (
    <ul className='summaryProduct-container'>
      <h3>Resumen de compra</h3>
      <div className="summaryProduct-detail">
        <li>{book.name}</li>
        <li>{book.price} CLP</li>
      </div>
      <div className="summaryProduct-seller">
        <li>Vendedor: Juan lopez</li>
      </div>
    </ul>
  )
}

export default SummaryProduct
