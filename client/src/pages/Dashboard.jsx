import { useEffect, useState } from "react";
import { getWorkspaces, createWorkspace, deleteWorkspace } from "../services/workspaceService";
import { Link } from "react-router-dom";

function Dashboard() {
    const [workspaces, setWorkspaces] = useState([]);
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");

    const handleCreate = async () => {
        if (!name.trim()) return;

        try {
            await createWorkspace({
                name,
                description,
            });

            setName("");
            setDescription("");

            loadWorkspaces();
        } catch (error) {
            console.error(error);
        }
    };
    useEffect(() => {
        loadWorkspaces();
    }, []);

    const loadWorkspaces = async () => {
        try {
            const data = await getWorkspaces();
            setWorkspaces(data);
        } catch (error) {
            console.error(error);
        }
    };
    const handleDelete = async (id) => {
        try {
            await deleteWorkspace(id);

            loadWorkspaces();
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div>
            <h1>AI Workbench</h1>

            <h2>Workspaces</h2>
            <div>
                <input
                    type="text"
                    placeholder="Workspace Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
                <button onClick={handleCreate}>
                    Create Workspace
                </button>
            </div>

            {workspaces.map((workspace) => (
                <div key={workspace._id}>
                    <Link to={`/workspace/${workspace._id}`}>
                        <h3>{workspace.name}</h3>
                    </Link>

                    <p>{workspace.description}</p>

                    <button
                        onClick={() => handleDelete(workspace._id)}
                    >
                        Delete
                    </button>
                </div>
            ))}
        </div>
    );
}

export default Dashboard;