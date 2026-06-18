import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { getWorkspaces, getRecentWorkspaces, createWorkspace, deleteWorkspace } from "../services/workspaceService";

function Dashboard() {

    const navigate = useNavigate();

    const [workspaces, setWorkspaces] = useState([]);

    const [recentWorkspaces, setRecentWorkspaces] = useState([]);

    const [name, setName] = useState("");

    const [description, setDescription] = useState("");

    const [searchTerm, setSearchTerm] = useState("");

    useEffect(() => {

        loadWorkspaces();
        loadRecentWorkspaces();

    }, []);

    const loadWorkspaces = async () => {

        try {

            const data =
                await getWorkspaces();

            setWorkspaces(data);

        } catch (error) {

            console.error(error);

        }
    };

    const loadRecentWorkspaces = async () => {

        try {

            const data =
                await getRecentWorkspaces();

            setRecentWorkspaces(data);

        } catch (error) {

            console.error(error);

        }
    };

    const handleCreate = async () => {

        if (!name.trim()) return;

        try {

            await createWorkspace({
                name,
                description
            });

            setName("");
            setDescription("");

            await loadWorkspaces();
            await loadRecentWorkspaces();

        } catch (error) {

            console.error(error);

        }
    };

    const handleDelete = async (workspaceId) => {

        const confirmed = window.confirm(
            "Delete this workspace?"
        );

        if (!confirmed) return;

        try {

            await deleteWorkspace(
                workspaceId
            );

            await loadWorkspaces();
            await loadRecentWorkspaces();

        } catch (error) {

            console.error(error);

        }
    };

    const filteredWorkspaces =
        workspaces.filter(
            (workspace) =>
                workspace.name
                    .toLowerCase()
                    .includes(
                        searchTerm.toLowerCase()
                    )
        );
    const handleLogout = () => {

        localStorage.removeItem(
            "token"
        );

        navigate("/login");

    };
    return (
        <div className="dashboard-container">

            <div className="dashboard-header">

                <h1>AI Workbench</h1>

                <button
                    onClick={handleLogout}
                >
                    Logout
                </button>

            </div>
            {/* SEARCH */}

            <input
                type="text"
                placeholder="Search workspaces..."
                value={searchTerm}
                onChange={(e) =>
                    setSearchTerm(
                        e.target.value
                    )
                }
            />
            <h2>Quick Start Templates</h2>

            <div className="template-grid">

                <div
                    className="template-card"
                    onClick={() =>
                        navigate("/resume-analyzer")
                    }
                >

                    <h3>
                        📄 Resume Analyzer
                    </h3>

                    <p>
                        Compare your resume
                        against a job
                        description and get
                        AI-powered feedback.
                    </p>

                </div>

                <div className="template-card"
                    onClick={() =>
                        navigate(
                            "/interview-prep"
                        )
                    }>

                    <h3>
                        🎯 Interview Prep
                    </h3>
                    <p>Prepare for your interviews</p>



                </div>

                <div className="template-card"
                    onClick={() =>
                        navigate(
                            "/resume-rewriter"
                        )}>

                    <h3>
                        🔬 Resume ReWriter
                    </h3>

                    <p>
                        Rewrite your resume tailored for a job description
                    </p>

                </div>

            </div>
            {/* RECENT WORKSPACES */}

            <h2>Recent Workspaces</h2>

            <div className="recent-workspaces">

                {recentWorkspaces.length === 0 ? (

                    <p>No recent workspaces.</p>

                ) : (

                    recentWorkspaces.map(
                        (workspace) => (

                            <div
                                key={workspace._id}
                                className="recent-card"
                                onClick={() =>
                                    navigate(
                                        `/workspace/${workspace._id}`
                                    )
                                }
                                style={{
                                    cursor: "pointer"
                                }}
                            >

                                <h4>
                                    {workspace.name}
                                </h4>

                                <p>
                                    {
                                        workspace.description
                                    }
                                </p>

                            </div>

                        )
                    )

                )}

            </div>

            {/* CREATE WORKSPACE */}

            <h2>Create Workspace</h2>

            <div className="create-workspace">

                <input
                    type="text"
                    placeholder="Workspace Name"
                    value={name}
                    onChange={(e) =>
                        setName(
                            e.target.value
                        )
                    }
                />

                <input
                    type="text"
                    placeholder="Description"
                    value={description}
                    onChange={(e) =>
                        setDescription(
                            e.target.value
                        )
                    }
                />

                <button
                    onClick={handleCreate}
                >
                    Create Workspace
                </button>

            </div>



            {/* ALL WORKSPACES */}

            <h2>All Workspaces</h2>

            {filteredWorkspaces.length === 0 ? (

                <p>No workspaces found.</p>

            ) : (

                filteredWorkspaces.map(
                    (workspace) => (

                        <div
                            key={workspace._id}
                            className="workspace-card"
                        >

                            <Link
                                to={`/workspace/${workspace._id}`}
                            >
                                <h3>
                                    {workspace.name}
                                </h3>
                            </Link>

                            <p>
                                {workspace.description}
                            </p>

                            <button
                                onClick={() =>
                                    handleDelete(
                                        workspace._id
                                    )
                                }
                            >
                                Delete
                            </button>

                        </div>

                    )
                )

            )}

        </div>
    );
}

export default Dashboard;