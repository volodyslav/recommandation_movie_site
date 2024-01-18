import axios from "axios"
import {  useState } from "react"
const Movie = () => {
    const [title, setTitle] = useState("")
    const [titleMovie, setTitleMovie] = useState(null);
    const [genre, setGenre] = useState(null);

    const submitData = async (e) => {
        e.preventDefault()
        try{
            const response = await axios.post("/predict", {title})

            console.log(response.data.data)
            if(response.status === 200){
                setTitleMovie(response.data.data["title"])
                setGenre(response.data.data["genres"])
            } else {
                console.error('Error:', response.statusText);
              }
        }catch(e){
            console.log(e)
        }
    }

    
  
    return (
    <div id="main">
        <h2 className="text-center text-4xl my-4 text-white">Movie Recommendation</h2>
        <form className="text-center space-x-4 my-6" onSubmit={submitData}>
            <input value={title} placeholder="Please put some title here" className="border border-gray-300 px-4 py-2 rounded-md w-2/3  mx-auto focus:outline-none focus:border-blue-500" onChange={(e) => setTitle(e.target.value)}/>
            <button type="submit" disabled={!title} className=" disabled:bg-slate-400 p-4 text-xl bg-green-700 rounded-lg focus:bg-green-500 hover:scale-110 duration-300 ease-in-out hover:bg-green-700 text-white">Search</button>
        </form>

        <div >
            {titleMovie !== null ? <div className="flex text-gray-700 bg-white p-10 rounded-2xl w-5/6  mx-auto shadow-xl">

                <ul className="w-full md:w-1/2 text-center">
                <span className="text-2xl  text-center mx-20">Title</span>
                {Object.keys(titleMovie).map((key, index) => (
                    <li key={index} className="mx-4">
                        {index+1}. {titleMovie[key]}
                        <hr></hr>
                    </li>
                ))}
                    
                </ul>
                <ul className=" hidden md:block text-center">
                <span className="text-2xl  text-center mx-6">Genres</span>
                {Object.keys(genre).map((key, index) => (
                    <li key={index} className="mx-4">
                    {index+1}. {genre[key]}
                        <hr></hr>
                    </li>
                ))}
                    
                </ul>

            </div> : ""}
        </div>
    </div>
  )
}

export default Movie