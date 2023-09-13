import { BackButton, InputFormBook } from '../'

import styles from './PublishBookForm.module.css'

export const PublishBookForm = () => {
  return (
    <div className={styles.publishBookFormContainer}>

      <BackButton />

      <form className={styles.publishBookForm}>

        <div className={styles.publishBookFormFlex}>
          <InputFormBook />
          <div className={styles.publishBookFormDown}>
            <label htmlFor="FormDescriptionBook">Descripción libro</label>
            <textarea placeholder='Escribe aquí...'></textarea>
          </div>
        </div>

        <div className={styles.publishBookButtonContainer}>
          <input className={styles.publishBookButton} type="submit" value='PUBLICAR' />
        </div>

      </form>

    </div>
  )
}
