import { InputLabelBook, SelectLabelBook } from '../'
import styles from './InputFormBook.module.css'

export const InputFormBook = () => {
  return (
    <div className={styles.publishBookFormUp}>

      <div className={styles.fileImgBookContainer}>
        <input type="file" />
      </div>

      <div className={styles.publishBookFormUpInfo}>

        <div className={styles.publishBookFormUpInfo1}>
          <InputLabelBook
            label='Nombre del libro'
            inputId='FormNameBook'
            placeholder='Ej: Dracula'
          />
          <InputLabelBook
            label='Nombre del autor'
            inputId='FormAutorBook'
            placeholder='Ej: Bram Stoker'
          />
        </div>
        <div className={styles.publishBookFormUpInfo2}>
          <InputLabelBook
            label='Precio del libro'
            inputId='FormPriceBook'
            placeholder='Ej: 10.000'
          />
          <SelectLabelBook inputId='FormGenreBook' label='Género' />

        </div>

      </div>

    </div>

  )
}
