const remote_host = "http://localhost:5000/";

export const getter = (resource, process, setLoading, setErr) => {
	const target = remote_host + resource;
	console.log("Starting get from ", target);
	fetch(target)
		.then((resp) => {
			if (!resp.ok) {
				throw new Error(`Status code from get()ing ${target}: ${resp.status}`);
			}
			return resp.json();
		})
		.then((json) => {
			console.log("Response to get from ", target, ": ", json);
			process(json);
			setLoading(false);
		})
		.catch((err) => {
			console.error("Error get()ing from ", target, ": ", err);
			setErr(err);
		});
};

export const poster = (resource, data, getTodos) => {
	const target = remote_host + resource;
	console.log("Starting POST to ", target);
	fetch(target, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(data),
	})
		.then((resp) => {
			if (!resp.ok) {
				throw new Error(`Status code from POSTing ${target}: ${resp.status}`);
			}
			return resp.json();
		})
		.then((json) => {
			console.log("Response to POST to ", target, ": ", json);
			// trigger re-poll
			getTodos();
		})
		.catch((err) => {
			console.log("Error POSTing to ", target, ": ", err);
		});
}
