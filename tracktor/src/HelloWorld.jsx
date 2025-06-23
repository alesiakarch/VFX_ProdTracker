import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function ListItem(props) {
  return (
  <li>
    {props.text} {props.IsDone && "✅"}
  </li>
  )
}

function List(props) {
  return (
    <ul>
      {props.list.map((item, index) => {
        return <ListItem key={index}
         text={item.text}
         IsDone={item.IsDone} />;
      })}
    </ul>
  );
}

function App() {
  const [count, setCount] = useState(0)
  const goals = [{text: "Make a Hello World webpage", IsDone: true},
                 {text:  "Learn React", IsDone: false},
                 {text: "Figure out the rest", IsDone: false}
                ]
  const food = [{text: "Pizza", IsDone: true},
                {text: "Sushi", IsDone: false},
                {text: "Chips", IsDone: false},
                {text: "Honey Pork", IsDone: true}
              ]
  

  return (
    <div>
      <h1>Hello World!</h1>
      <h2>This is my first website</h2>
      <h2>Goals:</h2>
      <List list = {goals} /> 
    </div>
  )
}

export default App
