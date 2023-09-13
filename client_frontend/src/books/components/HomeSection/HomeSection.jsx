import styles from './HomeSection.module.css'

export const HomeSection = ({ children, style }) => {
  return (
    <section className={`${styles.homeSection} ${styles[style] || ''}`}>
      <div className={styles.sectionContainer}>
        {children}
      </div>
    </section>
  )
}
