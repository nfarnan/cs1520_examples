import { useState, useEffect } from 'react'
import viteLogo from '/vite.svg';
import NewDo from './NewDo';
import Todos from './Todos';
import { getter } from './Utils';

const App = () => {
	const [todos, setTodos] = useState(null);
	const [loading, setLoading] = useState(true);
	const [err, setErr] = useState(null);

	useEffect(() => {getTodos();}, []);
	const getTodos = () => { getter("todos", setTodos, setLoading, setErr); };

	return (
  	<div className="App">
  		{ loading && <p>Loading...</p> }
  		{ err && <p>Failed to load!</p> }
  		{ !loading && <Todos todos={todos} getTodos={getTodos}/> }
  		<hr />
  		{ <NewDo getTodos={getTodos} /> }
  	</div>
	);
};

export default App;
