import { createContext, useContext, useEffect} from 'react';
import useFetch from '@/hooks/useFetch';

const ChangesContext = createContext();

export const ChangesProvider = ({ children }) => {
  const {data:changes, refetch:refetchChanges} = useFetch('/api/changes');
  
  useEffect(() => {
    const intervalo = setInterval(() => {
      refetchChanges();
    }, 5 * 60 * 1000); // 5 minutes

    return () => clearInterval(intervalo);
  }, [refetchChanges]);


  return (
    <ChangesContext.Provider value={{ changes, refetchChanges}}>
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
