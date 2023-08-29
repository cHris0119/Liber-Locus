import './HeroSection.css'
import HomeSection from '../HomeSection/HomeSection'

const HeroSection = () => {
  return (
    <HomeSection styles='home-hero'>
      <div className="hero-left">
        <h1 className='home-title'>¿Buscas libros al mejor precio?</h1>
        <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quo quos commodi asperiores! Autem nulla sunt, deserunt recusandae alias pariatur aliquid excepturi laudantium eos porro tempore, repudiandae fugiat tenetur minima mollitia?</p>
        <button className='hero-button'>Ir al marketplace</button>
      </div>
    </HomeSection>

  )
}

export default HeroSection
