import { HomeSection } from '../'
import SuscriptionsMock from '../../mocks/suscriptionsMock.json'

import styles from './Suscriptions.module.css'

export const Suscriptions = () => {
  const suscriptions = SuscriptionsMock.Suscriptions
  return (
    <HomeSection>
      <div className={styles.suscriptionsContainer}>
        <h2>Suscripciones</h2>
        <div className={styles.suscriptionsGrid}>
          {suscriptions.map((suscription) => (
            <article className={styles.suscription} key={suscription.id}>
              <div className={styles.suscriptionDetails}>
                <h3>{suscription.duration}</h3>
                <p>{suscription.price} CLP</p>
                <div className={styles.benefitsContainer}>
                  <div className={styles.benefits}>
                    <svg width="22" height="22" viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M11 0C8.82441 0 6.69767 0.645139 4.88873 1.85383C3.07979 3.06253 1.66989 4.78049 0.83733 6.79048C0.00476611 8.80047 -0.213071 11.0122 0.211367 13.146C0.635804 15.2798 1.68345 17.2398 3.22183 18.7782C4.76021 20.3165 6.72022 21.3642 8.85401 21.7886C10.9878 22.2131 13.1995 21.9952 15.2095 21.1627C17.2195 20.3301 18.9375 18.9202 20.1462 17.1113C21.3549 15.3023 22 13.1756 22 11C22 8.08262 20.8411 5.28472 18.7782 3.22182C16.7153 1.15892 13.9174 0 11 0ZM9.42857 15.3921L5.5 11.4636L6.74929 10.2143L9.42857 12.8936L15.2507 7.07143L16.5047 8.31757L9.42857 15.3921Z" fill="white"/>
                    </svg>
                    <p>Libros gratis</p>
                  </div>
                  <div className={styles.benefits}>
                    <svg width="22" height="22" viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M11 0C8.82441 0 6.69767 0.645139 4.88873 1.85383C3.07979 3.06253 1.66989 4.78049 0.83733 6.79048C0.00476611 8.80047 -0.213071 11.0122 0.211367 13.146C0.635804 15.2798 1.68345 17.2398 3.22183 18.7782C4.76021 20.3165 6.72022 21.3642 8.85401 21.7886C10.9878 22.2131 13.1995 21.9952 15.2095 21.1627C17.2195 20.3301 18.9375 18.9202 20.1462 17.1113C21.3549 15.3023 22 13.1756 22 11C22 8.08262 20.8411 5.28472 18.7782 3.22182C16.7153 1.15892 13.9174 0 11 0ZM9.42857 15.3921L5.5 11.4636L6.74929 10.2143L9.42857 12.8936L15.2507 7.07143L16.5047 8.31757L9.42857 15.3921Z" fill="white"/>
                    </svg>
                    <p>Libros gratis</p>
                  </div>

                </div>

              </div>
              <button className={styles.suscriptionButton}>Comprar ahora</button>
            </article>
          ))}
        </div>
      </div>
    </HomeSection>
  )
}