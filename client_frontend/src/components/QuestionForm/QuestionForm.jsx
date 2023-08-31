import './QuestionForm.css'

const QuestionForm = () => {
  return (
    <div className='questionForm-container'>
      <h3 style={{ color: '#fff' }}>Pregunta al vendedor</h3>
      <form className='questionForm'>
        <input className='questionForm-input' type="text" placeholder='Escribe tu pregunta' />
        <input className='questionForm-input' type="submit" name="" id="" value='Preguntar' />
      </form>
    </div>
  )
}

export default QuestionForm
