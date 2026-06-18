import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { getWorkspaces, getRecentWorkspaces, createWorkspace, deleteWorkspace, updateWorkspace } from "../services/workspaceService";

function Dashboard() {

    const navigate = useNavigate();

    const [workspaces, setWorkspaces] = useState([]);

    const [recentWorkspaces, setRecentWorkspaces] = useState([]);

    const [name, setName] = useState("");

    const [description, setDescription] = useState("");

    const [searchTerm, setSearchTerm] = useState("");
    const [editingId, setEditingId] = useState(null);

    const [editName, setEditName] = useState("");

    const [editDescription, setEditDescription] = useState("");

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

    const handleUpdate =
        async () => {

            try {

                await updateWorkspace(
                    editingId,
                    {
                        name: editName,
                        description:
                            editDescription
                    }
                );

                setEditingId(null);
                setEditName("");
                setEditDescription("");
                await loadWorkspaces();

                await loadRecentWorkspaces();

            } catch (error) {

                console.error(error);

            }
        };

    return (
        <div className="dashboard-container">
            <div className="dashboard-header">
                <div>
                    <h1>CogniDesk</h1>
                    <h3>AI-Powered Workspace for Research and Document Intelligence</h3>
                </div>
                <button onClick={handleLogout}>Logout</button>
            </div>

            {/* SEARCH BAR SPANS FULL WIDTH ABOVE PANELS */}
            <div className="search-wrapper">
                <input
                    type="text"
                    placeholder="Search workspaces..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>

            {/* NEW TWO-COLUMN SIDEBAR LAYOUT */}
            <div className="dashboard-grid-layout">

                {/* LEFT SIDEBAR: QUICK START TEMPLATES */}
                <aside className="dashboard-sidebar">
                    <h2>Quick Start</h2>
                    <div className="template-vertical-list">
                        <div className="template-card" onClick={() => navigate("/resume-analyzer")}>
                            <h3>📄 Resume Analyzer</h3>
                            <p>Compare your resume against a job description and get AI feedback.</p>
                        </div>

                        <div className="template-card" onClick={() => navigate("/interview-prep")}>
                            <h3>🎯 Interview Prep</h3>
                            <p>Prepare for your technical and behavioral interviews seamlessly.</p>
                        </div>

                        <div className="template-card" onClick={() => navigate("/resume-rewriter")}>
                            <h3>🔬 Resume ReWriter</h3>
                            <p>Rewrite your resume sections tailored precisely for a job description.</p>
                        </div>
                    </div>
                </aside>

                {/* RIGHT MAIN PANEL: ACTIONS & DATA */}
                <main className="dashboard-main-content">

                    {/* IMPROVED PREMIUM CREATE WORKSPACE BLOCK */}
                    <section className="create-workspace-hero">
                        <div className="hero-meta">
                            <h2>Initialize New Workspace</h2>
                            <p>Deploy a sandbox environment to extract entities, run vector embeddings, and interface with document context intelligence logs.</p>
                        </div>
                        <div className="create-fields-row">
                            <input
                                type="text"
                                placeholder="Workspace Name"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                            />
                            <input
                                type="text"
                                placeholder="Description of Workspace"
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                            />
                            <button onClick={handleCreate}>
                                Deploy Workspace Environment
                            </button>
                        </div>
                    </section>

                    {/* RECENT WORKSPACES */}
                    <h2>Recent Workspaces</h2>
                    <div className="recent-workspaces">
                        {recentWorkspaces.length === 0 ? (
                            <p className="empty-log-text">No active session deployments found.</p>
                        ) : (
                            recentWorkspaces.map((workspace) => (
                                <div
                                    key={workspace._id}
                                    className="recent-card"
                                    onClick={() => navigate(`/workspace/${workspace._id}`)}
                                    style={{ cursor: "pointer" }}
                                >
                                    <h4>{workspace.name}</h4>
                                    <p>{workspace.description}</p>
                                </div>
                            ))
                        )}
                    </div>

                    {/* ALL WORKSPACES */}
                    <h2>All System Workspaces</h2>
                    <div className="all-workspaces-list">
                        {filteredWorkspaces.length === 0 ? (
                            <p className="empty-log-text">No workspaces match queries.</p>
                        ) : (
                            filteredWorkspaces.map((workspace) => (

                                <div
                                    key={workspace._id}
                                    className="workspace-card"
                                >

                                    {
                                        editingId === workspace._id ? (

                                            <div className="edit-workspace-form">

                                                <input
                                                    type="text"
                                                    value={editName}
                                                    onChange={(e) =>
                                                        setEditName(
                                                            e.target.value
                                                        )
                                                    }
                                                />

                                                <input
                                                    type="text"
                                                    value={editDescription}
                                                    onChange={(e) =>
                                                        setEditDescription(
                                                            e.target.value
                                                        )
                                                    }
                                                />

                                                <div className="workspace-actions">

                                                    <button
                                                        onClick={handleUpdate}
                                                    >
                                                        Save
                                                    </button>

                                                    <button
                                                        onClick={() =>
                                                            setEditingId(null)
                                                        }
                                                    >
                                                        Cancel
                                                    </button>

                                                </div>

                                            </div>

                                        ) : (

                                            <>
                                                <div
                                                    className="card-link-wrapper"
                                                    onClick={() =>
                                                        navigate(
                                                            `/workspace/${workspace._id}`
                                                        )
                                                    }
                                                    style={{
                                                        cursor: "pointer",
                                                        flex: 1
                                                    }}
                                                >

                                                    <h3>
                                                        {workspace.name}
                                                    </h3>

                                                    <p>
                                                        {workspace.description}
                                                    </p>

                                                </div>

                                                <div className="workspace-actions">

                                                    <button
                                                        onClick={() => {

                                                            setEditingId(
                                                                workspace._id
                                                            );

                                                            setEditName(
                                                                workspace.name
                                                            );

                                                            setEditDescription(
                                                                workspace.description
                                                            );

                                                        }}
                                                    >
                                                        Edit
                                                    </button>

                                                    <button
                                                        onClick={(e) => {

                                                            e.stopPropagation();

                                                            handleDelete(
                                                                workspace._id
                                                            );

                                                        }}
                                                    >
                                                        Delete
                                                    </button>

                                                </div>
                                            </>

                                        )
                                    }

                                </div>

                            ))
                        )}
                    </div>

                </main>
            </div>
        </div>
    );
}

export default Dashboard;