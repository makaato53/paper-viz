import { useState } from "react";
import FileUpload from "../components/FileUpload";
import Results from "../components/Results";

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleAnalyze = async () => {
    if (!file) return;
    setIsAnalyzing(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/proxy", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Failed to analyze PDF:", err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <main className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Paper Analyzer</h1>
      <FileUpload onFileSelect={setFile} />
      <button
        onClick={handleAnalyze}
        disabled={!file || isAnalyzing}
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {isAnalyzing ? "Analyzing..." : "Analyze PDF"}
      </button>
      {result && <Results data={result} />}
    </main>
  );
}

