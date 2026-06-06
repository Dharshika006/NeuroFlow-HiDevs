"use client";

import { useState } from "react";

import PipelineSelector from "@/components/PipelineSelector";
import QueryPanel from "@/components/QueryPanel";
import CitationDrawer from "@/components/CitationDrawer";
import RetrievalInspector from "@/components/RetrievalInspector";

import { useSSEStream } from "@/hooks/useSSEStream";

export default function PlaygroundPage() {

  const [pipeline, setPipeline] =
    useState("default");

  const [pipelineB, setPipelineB] =
    useState("research");

  const [compareMode, setCompareMode] =
    useState(false);

  const [runId, setRunId] =
    useState("");

  const [

    selectedCitation,

    setSelectedCitation

  ] = useState<any>(null);

  const {

    tokens,

    citations

  } = useSSEStream(runId);

  const pipelines = [

    {
      id: "default",
      name: "Default",
      avg_score: 0.84
    },

    {
      id: "research",
      name: "Research",
      avg_score: 0.90
    }
  ];

  async function submit(
    query: string
  ) {

    try {

      const res = await fetch(

        "http://127.0.0.1:8000/query",

        {

          method: "POST",

          headers: {

            "Content-Type":
              "application/json"
          },

          body: JSON.stringify({

            query,

            pipeline_id:
              pipeline,

            stream: true
          })
        }
      );

      const data =
        await res.json();

      if (data.run_id) {

        setRunId(
          data.run_id
        );
      }

    } catch (err) {

      console.error(err);
    }
  }

  async function rateRun(
    rating: number
  ) {

    if (!runId)
      return;

    try {

      await fetch(

        `http://127.0.0.1:8000/runs/${runId}/rating`,

        {

          method: "PATCH",

          headers: {

            "Content-Type":
              "application/json"
          },

          body: JSON.stringify({

            rating
          })
        }
      );

    } catch (err) {

      console.error(err);
    }
  }

  return (

    <div className="p-6">

      <h1

        className="
        text-3xl
        font-bold
        mb-4"

      >

        Query Playground

      </h1>

      <PipelineSelector

        pipelines={pipelines}

        value={pipeline}

        onChange={setPipeline}
      />

      <div className="mt-4">

        <label>

          <input

            type="checkbox"

            checked={
              compareMode
            }

            onChange={(e) =>
              setCompareMode(
                e.target.checked
              )
            }
          />

          {" "}
          Compare Mode

        </label>

      </div>

      {

        compareMode && (

          <div
            className="mt-4"
          >

            <PipelineSelector

              pipelines={pipelines}

              value={pipelineB}

              onChange={
                setPipelineB
              }
            />

          </div>
        )
      }

      <div
        className="mt-6"
      >

        <QueryPanel
          onSubmit={submit}
        />

      </div>

      <div

        className="
        border
        rounded
        p-4
        mt-6
        min-h-[200px]"

      >

        <h3

          className="
          font-bold
          mb-2"

        >

          Response

        </h3>

        {tokens}

      </div>

      <div
        className="mt-4"
      >

        {citations.map(

          (

            c: any,

            idx: number

          ) => (

            <button

              key={idx}

              className="
              border
              px-2
              py-1
              mr-2
              rounded"

              onClick={() =>
                setSelectedCitation(
                  c
                )
              }
            >

              {

                c.reference ||

                `Source ${idx + 1}`
              }

            </button>
          )
        )}

      </div>

      <div className="mt-4">

        <button

          className="
          border
          px-3
          py-2
          mr-2
          rounded"

          onClick={() =>
            rateRun(5)
          }
        >

          👍 Helpful

        </button>

        <button

          className="
          border
          px-3
          py-2
          rounded"

          onClick={() =>
            rateRun(1)
          }
        >

          👎 Not Helpful

        </button>

      </div>

      <div className="mt-8">

        <RetrievalInspector />

      </div>

      <CitationDrawer

        citation={
          selectedCitation
        }

        onClose={() =>
          setSelectedCitation(
            null
          )
        }
      />

    </div>
  );
}