import './InputFormBook.css'
import { InputLabelBook, SelectLabelBook } from '../InputLabelBook/InputLabelBook'

const InputFormBook = () => {
  return (
    <div className="publishBookForm-up">

      <div className='fileImgBook-container'>
        <input type="file" />
      </div>

      <div className="publishBookForm-up-info">

        <div className="publishBookForm-up-info-1">
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

        <div className="publishBookForm-up-info-2">
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

export default InputFormBook
