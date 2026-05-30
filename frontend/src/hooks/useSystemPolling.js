import { useEffect, useRef } from "react";

export function useSystemPolling({
  checkApi,
  loadFacts,
  loadCapabilities,
  intervalMs = 30000,
}) {
  const runningRef = useRef(false);

  useEffect(() => {
    let stopped = false;

    async function runPoll() {
      if (runningRef.current || stopped) return;

      if (document.visibilityState === "hidden") {
        return;
      }

      runningRef.current = true;

      try {
        await Promise.allSettled([
          checkApi(),
          loadFacts(),
          loadCapabilities(),
        ]);
      } finally {
        runningRef.current = false;
      }
    }

    runPoll();

    const interval = setInterval(runPoll, intervalMs);

    function handleVisibilityChange() {
      if (document.visibilityState === "visible") {
        runPoll();
      }
    }

    document.addEventListener("visibilitychange", handleVisibilityChange);

    return () => {
      stopped = true;
      clearInterval(interval);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, [checkApi, loadFacts, loadCapabilities, intervalMs]);
}
