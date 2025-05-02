import { createContext, useContext, useEffect, useState} from 'react';
import useFetch from '@/hooks/useFetch';

const TradeRequestContext = createContext();

export const TradeRequestProvider = ({ children }) => {
  const {data, refetch:refetchTradeRequests} = useFetch('/api/trade-requests');
  const [fiatSuscriptions, setFiatSuscriptions] = useState([])
  const [tradeRequests, setTradeRequests] = useState([])

  const [buyRequests, setBuyRequests] = useState([])
  const [sellRequests, setSellRequests] = useState([])
  
  const [historyRequests, setHistoryRequests] = useState([])
  const [presentRequests, setPresentRequests] = useState([])

  const diferentiateRequestByStatus = () => {

    const { present, history } = tradeRequests.reduce(
      (acc, item) => {
          if (item.status < 3) {
            acc.present.push(item);
          } else if (item.status == 3) {
          acc.history.push(item);
          }
        return acc;
      },
      { present: [], history: [] }
    );

    setHistoryRequests(history)
    setPresentRequests(present)

  }


  const diferentiateRequestBySide = () => {
    const { buyIds, sellIds } = fiatSuscriptions.reduce(
      (acc, item) => {
        if (item.side === "B") {
          acc.buyIds.push(item.id);
        } else if (item.side === "S") {
          acc.sellIds.push(item.id);
        }
        return acc;
      },
      { buyIds: [], sellIds: [] }
    );

  const buys = [];
  const sells = [];

  presentRequests.forEach(item => {
    if (buyIds.includes(item.pair)) buys.push(item);
    else if (sellIds.includes(item.pair)) sells.push(item);
  });

  setBuyRequests(buys);
  setSellRequests(sells);

  }

  const updateTradeRequest = (tradeId, tradeObj) => {
    setTradeRequests((prevTrades) => 
      prevTrades.map((trade) => trade.id == tradeId ? tradeObj : trade)
    )
  }

  useEffect(() => {
    diferentiateRequestBySide()    
  }, [presentRequests])

  useEffect(() => {
    if(data) {
      setFiatSuscriptions(data.fiat_suscriptions)
      setTradeRequests(data.results)
    }
  }, [data])

  useEffect(() => {
    if (fiatSuscriptions?.length && tradeRequests?.length) {
      diferentiateRequestByStatus()
    }
  }, [fiatSuscriptions, tradeRequests]);

  useEffect(() => {
    const intervalo = setInterval(() => {
      refetchTradeRequests();
    }, 5 * 60 * 1000); // 5 minutes

    return () => clearInterval(intervalo);
  }, [refetchTradeRequests]);

  const insertNewTradeRequest = (trade) => {
    setTradeRequests((prev) => [...prev , trade ])
  }


  function getFiatPair(pairId) {
    const pair = fiatSuscriptions?.filter(pair => pair.id === pairId)[0]
    if (pair) return pair
  }

  return (
    <TradeRequestContext.Provider value={{ refetchTradeRequests, historyRequests, insertNewTradeRequest, updateTradeRequest, buyRequests, sellRequests, fiatSuscriptions, getFiatPair}}>
      {children}
    </TradeRequestContext.Provider>
  );
};

export const useTradeRequest = () => {
  const context = useContext(TradeRequestContext);
  if (!context) {
    throw new Error("useTradeRequest debe usarse dentro de CurrencyProvider");
  }
  return context;
};
