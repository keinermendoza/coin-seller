import { createContext, useContext, useEffect, useState} from 'react';
import useFetch from '@/hooks/useFetch';

const ChangesContext = createContext();

export const ChangesProvider = ({ children }) => {
  const {data:changes, refetch:refetchChanges} = useFetch('/api/changes');
  const [buyPairs, setBuyPairs] = useState([])
  const [sellPairs, setSellPairs] = useState([])
  const [requestTime, setRequestTime] = useState('')

  useEffect(() => {
    if(changes) {
      setBuyPairs(changes.buy)
      setSellPairs(changes.sell)
      setRequestTime(changes.now)
    }
  }, [changes])

  useEffect(() => {
    const intervalo = setInterval(() => {
      refetchChanges();
    }, 5 * 60 * 1000); // 5 minutes

    setBuyPairs()
    return () => clearInterval(intervalo);
  }, [refetchChanges]);


  return (
    <ChangesContext.Provider value={{ buyPairs, sellPairs, requestTime, refetchChanges}}>
      {children}
    </ChangesContext.Provider>
  );
};

export const useChanges = () => {
  const context = useContext(ChangesContext);
  if (!context) {
    throw new Error("useChanges debe usarse dentro de CurrencyProvider");
  }
  return context;
};
