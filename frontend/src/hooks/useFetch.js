import { useState, useEffect, useCallback } from 'react';
import axios from '@/lib/axios';

export default function useFetch(url, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const controller = new AbortController();

  const fetchData = useCallback(async () => {
    if (!url) return;

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
  }, [url, JSON.stringify(options)]); // JSON.stringify para asegurar que detecte cambios en las opciones

  useEffect(() => {
    fetchData();

    return () => {
      controller.abort();
    };
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}
