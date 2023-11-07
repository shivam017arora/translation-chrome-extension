import { useState } from "react";
import { getTranslation } from "~api/transalations";

function IndexPopup() {
  const [word, setWord] = useState("")
  const [translation, setTranslation] = useState("")
  const [targetLanguage, setTargetLanguage] = useState("Spanish")
  const [error, setError] = useState("")

  const fetchTranslation = async () => {
    // Reset error and translation
    setError("")
    setTranslation("")

    // Check if word is empty
    if (!word) {
      setError("Please enter a word")
      return
    }

    // Make API call
    try {
      const translation = await getTranslation(word, targetLanguage);
      console.log("translation: ", translation)
      setTranslation(translation['translation'])
    } catch (err) {
      setError(err.message)
      return
    }
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        padding: 16,
        width: 300
      }}>
      <h2>Translate Word</h2>
      <input
        placeholder="Enter word"
        onChange={(e) => setWord(e.target.value)}
        value={word}
        style={{ marginBottom: "10px" }}
      />
      <p>Select Target: </p>
      <select name="targetLanguage" id="targetLanguage" 
      value={targetLanguage} onChange={(e) => setTargetLanguage(e.target.value)}
      >
        <option value="spanish">Spanish</option>
        <option value="french">French</option>
        <option value="german">German</option>
      </select>

      <button onClick={fetchTranslation} style={{"marginTop": 10}}>Get Translation</button>
      {translation && <p>Translation: {translation}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  )
}

export default IndexPopup