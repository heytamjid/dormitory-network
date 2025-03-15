import Timer from './myComponents/Timer';

function App() { 
  return (
    <div className="flex items-start justify-between h-screen w-screen bg-[url('./media/launchpad.jpg')] bg-cover"> 
      <div className='border-0 border-black border-solid bg-blue-50/40 rounded-lg shadow-2xl my-8 mx-8 px-4 py-4'>
        <Timer />
      </div>
    </div>
  );
}

export default App;