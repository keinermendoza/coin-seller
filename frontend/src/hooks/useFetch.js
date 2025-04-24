import { useState, useEffect } from 'react';
import axios from "@/lib/axios";

export default function useFetch(url, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!url) return;

    const controller = new AbortController();
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await axios.get(url, {
          signal: controller.signal,
          ...options,
        });
        setData(response.data);
        setError(null);
      } catch (err) {
        if (!axios.isCancel(err)) {
          setError(err);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    return () => {
      controller.abort(); // cancela la petición si el componente se desmonta
    };
  }, [url]);

  return { data, loading, error };
}
