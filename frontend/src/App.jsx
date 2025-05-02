import { BrowserRouter, Routes, Route, Navigate } from "react-router";
import { BaseLayout, LayoutChanges, LayoutConfiguration, LayoutImages } from "./layouts";
import Edit from "@/pages/changes/Edit";
function App() {
  return (

  <BrowserRouter>
    <Routes>
      <Route path="client" element={<BaseLayout />} >
        <Route index element={<Navigate to="changes" replace />} /> 
        
        <Route path="changes" >
          <Route index element={<LayoutChanges />} /> 
          <Route path=":id" element={<Edit />} /> 
        </Route>

        <Route path="configuration" element={<LayoutConfiguration />} />
        <Route path="images" element={<LayoutImages />} />
      </Route>
    </Routes>
  </BrowserRouter>
  )
}

export default App
