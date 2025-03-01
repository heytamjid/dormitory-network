import Timer from './components/Timer';

function App() { //this calssName app-container is not defined in css file yet, but will be used later to rightly position and style the Timercomponent. 
  return (
    <div className="app-container "> 
      <Timer />
    </div>
  );
}

export default App;