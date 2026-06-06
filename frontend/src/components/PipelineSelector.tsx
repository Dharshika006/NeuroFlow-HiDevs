"use client";

type Props = {

  pipelines: any[];

  value: string;

  onChange: (
    value: string
  ) => void;
};

export default function PipelineSelector({

  pipelines,

  value,

  onChange

}: Props) {

  return (

    <select

      value={value}

      onChange={(e) =>
        onChange(
          e.target.value
        )
      }

      className="
      border
      p-2
      rounded
      w-full"
    >

      {pipelines.map(

        (p) => (

          <option

            key={p.id}

            value={p.id}
          >

            {p.name}
            {" "}
            (
            {p.avg_score}
            )

          </option>
        )
      )}

    </select>
  );
}