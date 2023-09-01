import './PublishBookForm.css'
import BackButton from '../BackButton/BackButton'
import InputFormBook from '../InputFormBook/InputFormBook'

const PublishBookForm = () => {
  return (
    <div className="publishBookForm-container">

      <BackButton />

      <form className='publishBookForm'>

        <div className='publishBookForm-flex'>

          <InputFormBook />

          <div className='publishBookForm-down'>
            <label htmlFor="FormDescriptionBook">Descripción libro</label>
            <textarea placeholder='Escribe aquí...'></textarea>
          </div>

        </div>
        <div className="publishBook-button-container">
          <input className='publishBookButton' type="submit" value='PUBLICAR' />
        </div>
      </form>

    </div>
  )
}

export default PublishBookForm
