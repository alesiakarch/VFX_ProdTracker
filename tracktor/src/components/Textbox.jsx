import { useState } from "react"


export function Textbox({className}) {

    const [text, setText] = useState("")

    return (
        <>
            <input className ={className} onChange={(e) => setText(e.target.value)}></input>
            <p>{text}</p>
        </>
    )
}