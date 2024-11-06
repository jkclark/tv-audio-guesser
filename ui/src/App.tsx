import "./App.css";
import sound from "./audio/s1/e1/the_ship_could_be_booby_trapped.mp3";

function App() {
  // const [count, setCount] = useState(0);

  const playSound = () => {
    const audio = new Audio(sound);
    audio.play();
  };

  return (
    <>
      <h1>Guess the episode from the audio</h1>
      <div>
        <button onClick={playSound}>Play Sound</button>
      </div>
    </>
  );
}

export default App;
