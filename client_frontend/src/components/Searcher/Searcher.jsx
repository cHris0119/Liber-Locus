import './Searcher.css'
const Searcher = () => {
  return (

    <form className='form-search'>
      <input type="text" className='searcher' placeholder='Busca un libro...' />
      <input type="submit" value='Buscar' />
    </form>

  )
}

export default Searcher
