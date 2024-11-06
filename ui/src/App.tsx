import sound from "../../audio/41_I'm_Hakoda,_Katara_and_So.mp3";
import "./App.css";

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
