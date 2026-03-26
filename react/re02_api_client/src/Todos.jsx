import { poster } from './Utils';

const Todos = ({ todos, getTodos }) => {
	return (
	<div>
		<h1>Todos:</h1>
		<table>
			<tbody>
				{ Object.entries(todos).map(([k, v]) => <Todo key={k} taskID={k} {...v} getTodos={getTodos}/>) }
			</tbody>
		</table>
	</div>
	);
};

const Todo = ({ taskID, task, done, getTodos }) => {
	const toggleTodo = () => {
		poster("mark", {"id": taskID, "status": !done}, getTodos);
	};
	return <tr>
		<td><input type="checkbox" checked={done} readOnly onClick={toggleTodo}/></td>
		<td>{task}</td>
	</tr>
};

export default Todos;
