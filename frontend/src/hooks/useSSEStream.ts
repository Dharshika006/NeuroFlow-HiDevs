"use client";

import { useEffect, useState } from "react";

export function useSSEStream(runId?: string) {

  const [tokens, setTokens] = useState("");

  const [done, setDone] = useState(false);

  const [citations, setCitations] = useState<any[]>([]);

  useEffect(() => {

    if (!runId) return;

    const es = new EventSource(
      `http://127.0.0.1:8000/query/${runId}/stream`
    );

    es.onmessage = (event) => {

      const data = JSON.parse(
        event.data
      );

      if (
        data.type === "token"
      ) {

        setTokens(
          prev => prev + data.delta
        );
      }

      if (
        data.type === "done"
      ) {

        setDone(true);

        setCitations(
          data.citations || []
        );

        es.close();
      }
    };

    return () => es.close();

  }, [runId]);

  return {
    tokens,
    done,
    citations
  };
}