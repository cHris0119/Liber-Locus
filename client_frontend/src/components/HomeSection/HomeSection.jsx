import './HomeSection.css'

const HomeSection = ({ children, styles }) => {
  return (
    <section className={`home-section ${styles || ''}`}>
      <div className="section-container">
        {children}
      </div>
    </section>
  )
}

export default HomeSection
