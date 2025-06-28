import { useState } from "react"


export function Textbox({className, value, onChange}) {

    const [text, setText] = useState("")

    return (
        <>
            <input className ={className} value={value} onChange={onChange}></input>
            <p>{text}</p>
        </>
    )
}