import React from 'react'; //importnat

const title = JSON.parse(document.getElementById('title').textContent);
const type = JSON.parse(document.getElementById('type').textContent);
console.log(title)
console.log(type)


const App = () => {
  return (
    <div>
      <h1>Hello, world!</h1>
      <p>Welcome to my React app.</p>
      <p>{title} and {type}</p>
    </div>
  );
}

export default App;