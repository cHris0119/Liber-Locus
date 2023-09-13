import styles from './Input.module.css'

export const Input = ({
  label,
  type,
  value,
  placeholder,
  error,
  name
}) => {
  return (
    <div className={styles.inputContainer}>
      <label
      htmlFor={name}
      className={styles.labelAuth}
      >
        {label}
      </label>
      <input
        id={name}
        type={type}
        name={name}
        value={value}
        placeholder={placeholder}
        className={styles.inputAuth}
      />
      {error && <span>{error}</span>}
    </div>
  )
}
