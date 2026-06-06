import Link from "next/link";

export default function Home() {
  return (
    <div style={{ padding: 20 }}>
      <h1>NeuroFlow</h1>

      <ul>
        <li><Link href="/playground">Playground</Link></li>
        <li><Link href="/pipelines">Pipelines</Link></li>
        <li><Link href="/evaluations">Evaluations</Link></li>
        <li><Link href="/documents">Documents</Link></li>
      </ul>
    </div>
  );
}