export default function StatusPill({ online }) {
  return (
    <div className="status-pill">
      <span className={online ? "dot online" : "dot offline"} />
      {online ? "API Online" : "API Offline"}
    </div>
  );
}
