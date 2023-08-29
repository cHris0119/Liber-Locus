import './Filters.css'

const Filters = () => {
  return (

    <div className="filters-container">
      <select className="filter">
        <option value="Recientes">Recientes</option>
        <option value="Antiguos">Antiguos</option>
      </select>
      <select className="filter">
        <option value="Menor a mayor">Menor a mayor</option>
        <option value="Mayor a menor">Mayor a menor</option>
      </select>
      <select className="filter">
        <option value="Todos">Todos</option>
        <option value="Terror">Terror</option>
        <option value="Romance">Romance</option>
      </select>
    </div>

  )
}

export default Filters
