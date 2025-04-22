import { BrowserRouter, Routes, Route, Navigate } from "react-router";
import { BaseLayout, LayoutChanges, LayoutConfiguration, LayoutImages } from "./layouts";

function App() {
  return (

  <BrowserRouter>
    <Routes>
      <Route path="client" element={<BaseLayout />} >
        <Route index element={<Navigate to="changes" replace />} /> 
        <Route path="changes" element={<LayoutChanges />} />
        <Route path="configuration" element={<LayoutConfiguration />} />
        <Route path="images" element={<LayoutImages />} />
      </Route>
    </Routes>
  </BrowserRouter>
  )
}

export default App
