import { useEffect, useMemo, useState } from "react";
import {
  ArrowRight,
  BookOpen,
  Brain,
  Clock3,
  Database,
  RefreshCw,
  Search,
  Sparkles,
  Tags,
} from "lucide-react";
import Panel from "../components/Panel";
import {
  getFacts,
  getMemoryOverview,
  getRecentMemories,
  searchMemory,
} from "../services/memoryService";

const SEARCH_SHORTCUTS = [
  "Laravel",
  "frontend",
  "SEO",
  "project context",
  "preferences",
  "memory",
];

function formatTag(tag) {
  return String(tag || "")
    .replace(/[-_]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function formatPayloadSummary(entry) {
  const pieces = [];

  if (entry?.source) pieces.push(`source ${entry.source}`);
  if (entry?.importance != null) pieces.push(`importance ${entry.importance}`);
  if (entry?.tags?.length) pieces.push(`${entry.tags.length} tags`);

  return pieces.length > 0 ? pieces.join(" • ") : "semantic memory";
}

export default function MemoryPanel() {
  const [overview, setOverview] = useState(null);
  const [facts, setFacts] = useState([]);
  const [memories, setMemories] = useState([]);
  const [query, setQuery] = useState("");
  const [searchResult, setSearchResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);

  async function loadData() {
    setLoading(true);
    try {
      const [overviewData, factsData, memoryData] = await Promise.all([
        getMemoryOverview(12),
        getFacts(),
        getRecentMemories(12),
      ]);

      setOverview(overviewData);
      setFacts(factsData.facts || overviewData.recent_facts || []);
      setMemories(memoryData.memories || overviewData.recent_memories || []);
    } catch {
      setOverview(null);
      setFacts([]);
      setMemories([]);
    } finally {
      setLoading(false);
    }
  }

  async function handleSearch(nextQuery = query) {
    const trimmed = nextQuery.trim();
    if (!trimmed) return;

    setSearchLoading(true);
    setQuery(trimmed);
    try {
      const data = await searchMemory(trimmed);
      setSearchResult(data.results || "No matching memory found.");
    } catch (error) {
      setSearchResult(`Memory search failed: ${error.message}`);
    } finally {
      setSearchLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  const stats = overview?.stats || {
    facts: facts.length,
    memories: memories.length,
    vector_memories: 0,
    semantic_index: 0,
  };

  const topTags = overview?.vector_summary?.top_tags || [];
  const sourceCounts = overview?.vector_summary?.source_counts || {};
  const vectorMemories = overview?.vector_memories || [];

  const sourceEntries = useMemo(
    () => Object.entries(sourceCounts).sort((a, b) => b[1] - a[1]),
    [sourceCounts],
  );

  return (
    <Panel title="Memory Command Center" icon={<Database />}>
      <div className="memory-shell">
        <div className="memory-hero">
          <div className="memory-hero-copy">
            <p className="memory-eyebrow">SEMANTIC + FACT MEMORY</p>
            <h2>Jarvis Memory Atlas</h2>
            <p className="memory-subtitle">
              Search what Jarvis knows, inspect semantic memory health, and review the latest
              facts and long-term context without leaving the workstation.
            </p>
          </div>

          <div className={`memory-status ${loading ? "warming" : "ready"}`}>
            <Brain size={16} />
            {loading ? "Synchronizing memory" : "Memory online"}
          </div>
        </div>

        <div className="memory-metrics">
          <div className="memory-metric">
            <span>Facts</span>
            <strong>{stats.facts ?? 0}</strong>
          </div>

          <div className="memory-metric">
            <span>Recent memory</span>
            <strong>{stats.memories ?? 0}</strong>
          </div>

          <div className="memory-metric">
            <span>Semantic index</span>
            <strong>{stats.semantic_index ?? 0}</strong>
          </div>

          <div className="memory-metric">
            <span>Active vector memories</span>
            <strong>{stats.vector_memories ?? 0}</strong>
          </div>
        </div>

        <div className="memory-toolbar memory-toolbar--premium">
          <div className="memory-search">
            <Search size={16} />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search memory, facts, preferences, project context..."
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  event.preventDefault();
                  handleSearch();
                }
              }}
            />
            <button onClick={() => handleSearch()} disabled={searchLoading || loading}>
              <Search size={16} />
              Search
            </button>
          </div>

          <button onClick={loadData} disabled={loading}>
            <RefreshCw size={16} />
            Refresh Memory
          </button>
        </div>

        <div className="memory-shortcuts">
          {SEARCH_SHORTCUTS.map((shortcut) => (
            <button
              key={shortcut}
              className="memory-shortcut"
              onClick={() => handleSearch(shortcut)}
              disabled={searchLoading || loading}
            >
              <Sparkles size={14} />
              {shortcut}
            </button>
          ))}
        </div>

        <div className="memory-workspace">
          <section className="memory-column">
            <div className="memory-card memory-search-card">
              <div className="memory-card-header">
                <div>
                  <h3>Semantic Search</h3>
                  <p>Query the memory stack and inspect the most relevant recall path.</p>
                </div>
                <span className="memory-card-chip">
                  <Clock3 size={12} />
                  Live
                </span>
              </div>

              <div className="memory-result-box">
                <pre>{searchResult || "Search memory to inspect matching entries here."}</pre>
              </div>
            </div>

            <div className="memory-card">
              <div className="memory-card-header">
                <div>
                  <h3>Saved Facts</h3>
                  <p>Fact memory should feel like a working notebook, not a dump.</p>
                </div>
                <span className="memory-card-chip">
                  <BookOpen size={12} />
                  {facts.length} entries
                </span>
              </div>

              <div className="memory-list">
                {facts.length === 0 && <p>No saved facts yet.</p>}
                {facts.map((fact) => (
                  <article key={fact.id} className="memory-item">
                    <strong>{fact.fact}</strong>
                    <span>{fact.created_at}</span>
                  </article>
                ))}
              </div>
            </div>
          </section>

          <section className="memory-column">
            <div className="memory-card">
              <div className="memory-card-header">
                <div>
                  <h3>Semantic Index</h3>
                  <p>Active vector memories, source distribution, and tag signal.</p>
                </div>
                <span className="memory-card-chip">
                  <Tags size={12} />
                  {topTags.length} top tags
                </span>
              </div>

              <div className="memory-tags">
                {topTags.length === 0 && <p>No tagged semantic memories yet.</p>}
                {topTags.map((item) => (
                  <span key={item.tag} className="memory-tag">
                    {formatTag(item.tag)} · {item.count}
                  </span>
                ))}
              </div>

              <div className="memory-source-list">
                {sourceEntries.length === 0 && <p>No vector sources registered yet.</p>}
                {sourceEntries.map(([source, count]) => (
                  <div key={source} className="memory-source-item">
                    <span>{source}</span>
                    <strong>{count}</strong>
                  </div>
                ))}
              </div>
            </div>

            <div className="memory-card">
              <div className="memory-card-header">
                <div>
                  <h3>Recent Memory</h3>
                  <p>Latest conversations and stored responses for fast review.</p>
                </div>
                <span className="memory-card-chip">
                  <ArrowRight size={12} />
                  Recent
                </span>
              </div>

              <div className="memory-list memory-list--tight">
                {memories.length === 0 && <p>No recent memory yet.</p>}
                {memories.map((memory) => (
                  <article key={memory.id} className="memory-item memory-item--large">
                    <div className="memory-item-head">
                      <strong>{memory.user_input}</strong>
                      <span>{memory.created_at}</span>
                    </div>
                    <p>{memory.jarvis_response}</p>
                  </article>
                ))}
              </div>
            </div>

            <div className="memory-card">
              <div className="memory-card-header">
                <div>
                  <h3>Vector Memory Ledger</h3>
                  <p>The highest-value semantic memories sorted by importance.</p>
                </div>
                <span className="memory-card-chip">
                  <Sparkles size={12} />
                  {vectorMemories.length} visible
                </span>
              </div>

              <div className="memory-ledger">
                {vectorMemories.length === 0 && <p>No vector memories available yet.</p>}
                {vectorMemories.map((entry) => (
                  <article key={entry.id} className="memory-ledger-item">
                    <div className="memory-ledger-head">
                      <strong>{entry.id}</strong>
                      <span>Importance {entry.importance ?? "—"}</span>
                    </div>
                    <p>{entry.text}</p>
                    <div className="memory-ledger-foot">
                      <span>{formatPayloadSummary(entry)}</span>
                      <span>{entry.created_at}</span>
                    </div>
                  </article>
                ))}
              </div>
            </div>
          </section>
        </div>
      </div>
    </Panel>
  );
}
