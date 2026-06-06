"use client";

import {

  ReactFlow,

  Background

} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

export default function RetrievalInspector() {

  const nodes = [

    {
      id: "1",
      position: {
        x: 0,
        y: 0
      },
      data: {
        label: "Query"
      },
      type: "default"
    },

    {
      id: "2",
      position: {
        x: 250,
        y: 0
      },
      data: {
        label:
          "Dense Retrieval"
      },
      type: "default"
    },

    {
      id: "3",
      position: {
        x: 250,
        y: 100
      },
      data: {
        label:
          "Sparse Retrieval"
      },
      type: "default"
    },

    {
      id: "4",
      position: {
        x: 500,
        y: 50
      },
      data: {
        label:
          "RRF Fusion"
      },
      type: "default"
    },

    {
      id: "5",
      position: {
        x: 750,
        y: 50
      },
      data: {
        label:
          "Reranker"
      },
      type: "default"
    }
  ];

  const edges = [

    {
      id: "e1",
      source: "1",
      target: "2"
    },

    {
      id: "e2",
      source: "1",
      target: "3"
    },

    {
      id: "e3",
      source: "2",
      target: "4"
    },

    {
      id: "e4",
      source: "3",
      target: "4"
    },

    {
      id: "e5",
      source: "4",
      target: "5"
    }
  ];

  return (

    <div
      style={{
        height: 500
      }}
    >

      <ReactFlow

        nodes={nodes}

        edges={edges}
      >

        <Background />

      </ReactFlow>

    </div>
  );
}