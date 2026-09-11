import { useEffect, useState } from "react";

/**
 * Small shared hook so every page follows the same
 * loading -> success / error -> render pattern, without repeating
 * boilerplate on each page.
 */
export function useApiData(fetchFn, deps = []) {
  const [data, setData] = useState(null);
  const [status, setStatus] = useState("loading"); // 'loading' | 'success' | 'error'
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;
    setStatus("loading");

    fetchFn()
      .then((result) => {
        if (!isMounted) return;
        setData(result);
        setStatus("success");
      })
      .catch((err) => {
        if (!isMounted) return;
        setError(err.message || "Something went wrong");
        setStatus("error");
      });

    return () => {
      isMounted = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return { data, status, error };
}
