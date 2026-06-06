"use client";

import { useState, useEffect } from "react";

import AnalyticsCharts from "@/components/AnalyticsCharts";
import PipelineEditor from "@/components/PipelineEditor";

export default function PipelinesPage() {

  const [pipelines, setPipelines] =
    useState<any[]>([]);

  const [

    selectedPipeline,

    setSelectedPipeline

  ] = useState<any>(null);

  const [

    showCreate,

    setShowCreate

  ] = useState(false);

  const [

    config,

    setConfig

  ] = useState(
    JSON.stringify(
      {
        name: "new-pipeline",
        description: "Pipeline",
        retrieval: {
          dense_k: 20
        }
      },
      null,
      2
    )
  );

  useEffect(() => {

    async function load() {

      try {

        const res =
          await fetch(
            "http://127.0.0.1:8000/pipelines"
          );

        const data =
          await res.json();

        if (
          Array.isArray(data)
        ) {

          setPipelines(data);

        } else {

          setPipelines([
            {
              id: "1",
              name: "Default",
              version: 1,
              avg_score: 0.84
            }
          ]);
        }

      } catch {

        setPipelines([
          {
            id: "1",
            name: "Default",
            version: 1,
            avg_score: 0.84
          }
        ]);
      }
    }

    load();

  }, []);

  async function savePipeline() {

    try {

      await fetch(

        "http://127.0.0.1:8000/pipelines",

        {

          method: "POST",

          headers: {

            "Content-Type":
              "application/json"
          },

          body: config
        }
      );

      setShowCreate(
        false
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

        Pipeline Manager

      </h1>

      <button

        className="
        border
        px-4
        py-2
        rounded
        mb-6"

        onClick={() =>
          setShowCreate(true)
        }

      >

        Create Pipeline

      </button>

      {

        pipelines.map(

          (p: any) => (

            <div

              key={p.id}

              className="
              border
              rounded
              p-4
              mb-4"

            >

              <h2

                className="
                text-xl
                font-semibold"

              >

                {p.name}

              </h2>

              <p>

                Version:
                {" "}
                {p.version}

              </p>

              <p>

                Avg Score:
                {" "}
                {p.avg_score}

              </p>

              <button

                className="
                mt-2
                border
                px-3
                py-1
                rounded"

                onClick={() =>
                  setSelectedPipeline(
                    p
                  )
                }

              >

                Analytics

              </button>

            </div>
          )
        )
      }

      {

        selectedPipeline && (

          <div

            className="
            fixed
            top-0
            right-0
            h-full
            w-96
            bg-white
            border-l
            shadow-lg
            p-4
            overflow-auto"

          >

            <button

              className="
              border
              px-2
              py-1"

              onClick={() =>
                setSelectedPipeline(
                  null
                )
              }

            >

              Close

            </button>

            <h2

              className="
              text-xl
              mt-4"

            >

              {
                selectedPipeline.name
              }

            </h2>

            <AnalyticsCharts

              data={[

                {
                  name: "P50",
                  value: 100
                },

                {
                  name: "P95",
                  value: 250
                },

                {
                  name: "P99",
                  value: 450
                }

              ]}

            />

          </div>
        )
      }

      {

        showCreate && (

          <div

            className="
            fixed
            inset-0
            bg-black/40
            flex
            items-center
            justify-center"

          >

            <div

              className="
              bg-white
              p-4
              rounded
              w-[900px]
              max-h-[90vh]
              overflow-auto"

            >

              <h2

                className="
                text-xl
                mb-4"

              >

                Create Pipeline

              </h2>

              <PipelineEditor

                value={config}

                onChange={setConfig}

              />

              <div
                className="mt-4"
              >

                <button

                  className="
                  border
                  px-4
                  py-2
                  mr-2"

                  onClick={
                    savePipeline
                  }

                >

                  Save

                </button>

                <button

                  className="
                  border
                  px-4
                  py-2"

                  onClick={() =>
                    setShowCreate(
                      false
                    )
                  }

                >

                  Cancel

                </button>

              </div>

            </div>

          </div>
        )
      }

    </div>
  );
}