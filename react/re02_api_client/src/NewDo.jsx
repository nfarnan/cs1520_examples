import { useState } from 'react';
import { poster } from './Utils';

const NewDo = ({ getTodos }) => {
	const [taskForm, setTaskForm] = useState("");

	const handleSubmit = (e) => {
		e.preventDefault();
		const formData = new FormData(e.target);
		const formJson = Object.fromEntries(formData.entries());
		poster("todos", formJson, getTodos);
		setTaskForm("");
	};	

	return (
		<form onSubmit={handleSubmit}>
			<label>
				New task: <input type="text" name="task" value={taskForm} onChange={(e) => setTaskForm(e.target.value)} />
			</label>
			<br />
			<input type="submit" value="Submit" />
		</form>
	);
};

export default NewDo;
