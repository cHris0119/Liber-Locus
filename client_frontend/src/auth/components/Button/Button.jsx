import styles from './Button.module.css'

export const Button = ({ buttonText, backgroundColor, textColor }) => {
  return (
    <button
      style={{ background: backgroundColor, color: textColor }}
      className={styles.button}
      type="submit"
    >
      {buttonText}
    </button>
  )
}
