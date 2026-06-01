import { useEffect, useState } from "react";
import { Database, RefreshCw, Search } from "lucide-react";
import Panel from "../components/Panel";
import { getFacts, getRecentMemories, searchMemory } from "../services/memoryService";


export default function MemoryPanel() {
  const [facts, setFacts] = useState([]);
  const [memories, setMemories] = useState([]);
  const [query, setQuery] = useState("");
  const [searchResult, setSearchResult] = useState("");
  const [loading, setLoading] = useState(false);

  async function loadData() {
    setLoading(true);
    try {
      const [factsData, memoryData] = await Promise.all([
        getFacts(),
        getRecentMemories(20),
      ]);
      setFacts(factsData.facts || []);
      setMemories(memoryData.memories || []);
    } finally {
      setLoading(false);
    }
  }

  async function handleSearch() {
    const trimmed = query.trim();
    if (!trimmed) return;

    setLoading(true);
    try {
      const data = await searchMemory(trimmed);
      setSearchResult(data.results || "No results found.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  return (
    <Panel title="Memory Console" icon={<Database />}>
      <div className="memory-toolbar">
        <div className="memory-search">
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search memory..."
          />
          <button onClick={handleSearch} disabled={loading}>
            <Search size={16} />
            Search
          </button>
        </div>

        <button onClick={loadData} disabled={loading}>
          <RefreshCw size={16} />
          Refresh
        </button>
      </div>

      <div className="logs-layout">
        <section className="panel-surface">
          <h3>Saved Facts</h3>
          <div className="memory-list">
            {facts.length === 0 && <p>No saved facts yet.</p>}
            {facts.map((fact) => (
              <div key={fact.id} className="memory-item">
                <strong>{fact.fact}</strong>
                <span>{fact.created_at}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="panel-surface">
          <h3>Recent Memory</h3>
          <div className="memory-list">
            {memories.length === 0 && <p>No recent memory yet.</p>}
            {memories.map((memory) => (
              <div key={memory.id} className="memory-item">
                <strong>{memory.user_input}</strong>
                <span>{memory.created_at}</span>
                <pre>{memory.jarvis_response}</pre>
              </div>
            ))}
          </div>
        </section>
      </div>

      <section className="panel-surface">
        <h3>Search Result</h3>
        <div className="result-box">
          <pre>{searchResult || "Search memory to inspect matching entries here."}</pre>
        </div>
      </section>
    </Panel>
  );
}
