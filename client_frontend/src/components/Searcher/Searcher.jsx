import styles from './Searcher.module.css'

export const Searcher = () => {
  return (

    <form className={styles.formSearch}>
      <input type="text" className='searcher' placeholder='Busca un libro...' />
      <input type="submit" value='Buscar' />
    </form>

  )
}
