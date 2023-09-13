import { HomeSection } from '../'

import styles from './HeroSection.module.css'

export const HeroSection = () => {
  return (
    <HomeSection style='homeHero'>
      <div className={styles.heroLeft}>
        <h1 className={styles.homeTitle}>¿Buscas libros al mejor precio?</h1>
        <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quo quos commodi asperiores! Autem nulla sunt, deserunt recusandae alias pariatur aliquid excepturi laudantium eos porro tempore, repudiandae fugiat tenetur minima mollitia?</p>
        <button className={styles.heroButton}>Ir al marketplace</button>
      </div>
    </HomeSection>

  )
}
