"use client";

import { useEffect, useState } from "react";

import EvaluationCard
from "@/components/EvaluationCard";

export default function EvaluationsPage() {

  const [

    evaluations,

    setEvaluations

  ] = useState<any[]>([]);

  const [

    connected,

    setConnected

  ] = useState(false);

  useEffect(() => {

    const eventSource =
      new EventSource(

        "http://127.0.0.1:8000/evaluations/stream"
      );

    eventSource.onopen = () => {

      setConnected(true);
    };

    eventSource.onmessage = (
      event
    ) => {

      try {

        const data =
          JSON.parse(
            event.data
          );

        setEvaluations(

          (prev) => [

            data,

            ...prev
          ]
        );

      } catch (

        err

      ) {

        console.error(
          err
        );
      }
    };

    eventSource.onerror = () => {

      setConnected(false);

      eventSource.close();
    };

    return () => {

      eventSource.close();
    };

  }, []);

  return (

    <div className="p-6">

      <h1

        className="
        text-3xl
        font-bold
        mb-4"

      >

        Evaluations

      </h1>

      <div
        className="mb-4"
      >

        Status:

        {" "}

        {

          connected

            ? "🟢 Connected"

            : "🔴 Waiting for stream"
        }

      </div>

      {

        evaluations.length === 0

          ? (

            <div

              className="
              border
              rounded
              p-4"

            >

              Waiting for evaluation events...

            </div>

          )

          : (

            evaluations.map(

              (

                evaluation,

                idx

              ) => (

                <EvaluationCard

                  key={idx}

                  evaluation={
                    evaluation
                  }

                />

              )
            )
          )
      }

    </div>
  );
}