import { use, useState } from "react";
import { Textbox } from "../components/Textbox";
import { Button } from "../components/Button";

export function LoginPage() {


    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    return (
        <div>
            <h1>Titles of the page</h1>
            <label>
                Username:
                <Textbox className={"bg-gray-200"} 
                value={username}
                onChange={(e) => setUsername(e.target.value)}/>
            </label>
            <br></br>
            <label>
                Password:
                <Textbox className={"bg-gray-200"}
                 value={password}
                 onChange={(e) => setPassword(e.target.value)}/>
            </label>
            <br></br>
            <Button title={"Login"} onClick={TakeToProjects}/>
        </div>
    )
}