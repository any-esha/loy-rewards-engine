import { useEffect, useState } from 'react'

export function useApi(load, fallback) {
  const [data, setData] = useState(fallback)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let mounted = true
    setLoading(true)
    load()
      .then((result) => mounted && setData(result))
      .catch((reason) => mounted && setError(reason.message || 'Unable to load data'))
      .finally(() => mounted && setLoading(false))
    return () => { mounted = false }
  }, [load])

  return { data, loading, error }
}
