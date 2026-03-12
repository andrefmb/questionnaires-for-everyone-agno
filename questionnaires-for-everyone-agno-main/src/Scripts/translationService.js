const baseURL = import.meta.env.VITE_API_URL

const translate = async (text, from, to) => {
  const response = await fetch(`${baseURL}/translate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      data: text,
      listType: 'single',
      sourceLang: from,
      targetLang: to
    }),
  })

  if (!response.ok) {
    const errorBody = await response.json()
    throw new Error(errorBody.error || `Translation failed with status ${response.status}`)
  }

  const result = await response.json()
  return result.translated
}

const evaluate = async (original, translation, backTranslation, originalLang, targetLang) => {
  const response = await fetch(`${baseURL}/evaluate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      listType: "single",
      sourceItems: original,
      newItems: translation,
      backtranslatedItems: backTranslation,
      sourceLang: originalLang,
      targetLang: targetLang
    })
  })

  if (!response.ok) {
    const errorBody = await response.json()
    throw new Error(errorBody.error || `Evaluation failed with status ${response.status}`)
  }

  const result = await response.json()
  return result // result contains { gemba, semantic }
}

export { translate, evaluate }