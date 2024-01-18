import Movie from "./components/Movie"
import axios from "axios"
axios.defaults.baseURL ="http://localhost:8000"
axios.defaults.withCredentials = true

function App() {

  return (
    <>
      <Movie></Movie>
    </>
  )
}

export default App
