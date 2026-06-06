"use client";

export default function EvaluationCard({

 evaluation

}: any) {

 return (

  <div
   className="
   border
   rounded
   p-4
   mb-4"
  >

   <h3>

    {evaluation.query}

   </h3>

   <div>

    <p>

     Faithfulness:
     {" "}
     {
      (
       evaluation.faithfulness * 100
      ).toFixed(0)
     }%

    </p>

    <progress

      max="1"

      value={
       evaluation.faithfulness
      }

    />

   </div>

   <div>

    <p>

     Relevance:
     {" "}
     {
      (
       evaluation.answer_relevance * 100
      ).toFixed(0)
     }%

    </p>

    <progress

      max="1"

      value={
       evaluation.answer_relevance
      }

    />

   </div>

   <div>

    <p>

     Overall:
     {" "}
     {
      (
       evaluation.overall_score * 100
      ).toFixed(0)
     }%

    </p>

   </div>

  </div>
 );
}