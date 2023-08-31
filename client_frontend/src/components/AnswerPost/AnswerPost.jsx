import './AnswerPost.css'
import lastQuestions from '../../mocks/lastQuestions.json'

const RenderQuestions = () => {
  const lastTenQuestions = lastQuestions.Questions.slice(1, 4)
  return (
    lastTenQuestions.map((question) => (
      <div className='lastAnswer' key={question.id}>
        <p className='lastAnswer-question'>{question.question}</p>
        {question.answer
          ? <div className="lastAnswer-answer-container">
            <p className='lastAnswer-answer'>{question.answer}</p><span className='lastAnswer-date'>{question.created_at}</span>
          </div>
          : <form className='form-answer'>
            <input type="text" placeholder='...' />
            <input type="submit" value='Responder' />
          </form>}

      </div>
    ))
  )
}

const AnswerPost = () => {
  return (
    <div className='answer-container'>
      <h3 style={{ color: '#fff' }} >Ultimas respuestas</h3>
      <RenderQuestions />
    </div>
  )
}

export default AnswerPost
