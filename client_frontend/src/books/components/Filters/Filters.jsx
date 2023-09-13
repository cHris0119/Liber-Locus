import styles from './Filters.module.css'

export const Filters = () => {
  return (

    <div className={styles.filtersContainer}>
      <select className={styles.filter}>
        <option value="Recientes">Recientes</option>
        <option value="Antiguos">Antiguos</option>
      </select>
      <select className={styles.filter}>
        <option value="Menor a mayor">Menor a mayor</option>
        <option value="Mayor a menor">Mayor a menor</option>
      </select>
      <select className={styles.filter}>
        <option value="Todos">Todos</option>
        <option value="Terror">Terror</option>
        <option value="Romance">Romance</option>
      </select>
    </div>

  )
}
