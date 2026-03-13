import { useEffect, useMemo, useState } from "react";

import { analyzeJob, fetchResumes, uploadResume } from "./api";

const defaultJobDescription = `We are hiring an AI/ML Engineer to build resume intelligence features. You should be strong in Python, FastAPI, PostgreSQL, React, Tailwind CSS, NLP, and LLM integration. Experience with Docker, cloud deployment, and production APIs is preferred.`;

function SkillPill({ label, tone = "neutral" }) {
  const toneClass = {
    neutral: "bg-white/80 border-slate-300 text-slate-700",
    good: "bg-emerald-100 border-emerald-300 text-emerald-900",
    gap: "bg-orange-100 border-orange-300 text-orange-900",
  }[tone];

  return (
    <span className={`inline-flex items-center rounded-full border px-3 py-1 text-sm ${toneClass}`}>
      {label}
    </span>
  );
}

function Panel({ title, subtitle, children }) {
  return (
    <section className="rounded-3xl border border-white/70 bg-white/70 p-5 shadow-glow backdrop-blur-md">
      <h2 className="text-xl font-semibold tracking-tight">{title}</h2>
      <p className="mt-1 text-sm text-slate-600">{subtitle}</p>
      <div className="mt-4">{children}</div>
    </section>
  );
}

export default function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [resumes, setResumes] = useState([]);
  const [uploadedResume, setUploadedResume] = useState(null);
  const [selectedResumeId, setSelectedResumeId] = useState("");

  const [jobTitle, setJobTitle] = useState("AI/ML Engineer");
  const [jobDescription, setJobDescription] = useState(defaultJobDescription);

  const [analysis, setAnalysis] = useState(null);
  const [loadingUpload, setLoadingUpload] = useState(false);
  const [loadingMatch, setLoadingMatch] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    void refreshResumes();
  }, []);

  const activeResumeId = useMemo(() => {
    if (uploadedResume?.resume_id) {
      return uploadedResume.resume_id;
    }
    return selectedResumeId ? Number(selectedResumeId) : null;
  }, [uploadedResume, selectedResumeId]);

  async function refreshResumes() {
    try {
      const data = await fetchResumes();
      setResumes(data);
    } catch {
      // Backend might be offline while frontend starts.
    }
  }

  async function handleUpload(event) {
    event.preventDefault();
    if (!resumeFile) {
      setError("Select a PDF resume first.");
      return;
    }

    setError("");
    setLoadingUpload(true);

    try {
      const result = await uploadResume(resumeFile);
      setUploadedResume(result);
      setSelectedResumeId(String(result.resume_id));
      setAnalysis(null);
      await refreshResumes();
    } catch (uploadError) {
      setError(uploadError.message || "Could not upload resume.");
    } finally {
      setLoadingUpload(false);
    }
  }

  async function handleAnalyze(event) {
    event.preventDefault();

    if (!activeResumeId) {
      setError("Upload a resume or choose one from the list.");
      return;
    }

    if (jobDescription.trim().length < 20) {
      setError("Job description must be at least 20 characters.");
      return;
    }

    setError("");
    setLoadingMatch(true);

    try {
      const result = await analyzeJob({
        resume_id: activeResumeId,
        job_title: jobTitle || null,
        job_description: jobDescription,
      });
      setAnalysis(result);
    } catch (analysisError) {
      setError(analysisError.message || "Could not analyze match.");
    } finally {
      setLoadingMatch(false);
    }
  }

  const score = Math.round(analysis?.match_percentage ?? 0);
  const scoreStyle = {
    background: `conic-gradient(var(--accent) ${score}%, rgba(15, 118, 110, 0.15) ${score}% 100%)`,
  };

  return (
    <div className="min-h-screen px-4 py-8 text-ink md:px-8">
      <div className="pointer-events-none fixed inset-0 -z-10">
        <div className="orb orb-a" />
        <div className="orb orb-b" />
      </div>

      <main className="mx-auto max-w-6xl space-y-6">
        <header className="rounded-3xl border border-white/70 bg-white/70 p-6 shadow-glow backdrop-blur-md">
          <p className="font-mono text-xs uppercase tracking-[0.24em] text-slate-500">Project 1</p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight md:text-4xl">
            AI Resume Analyzer and Job Matcher
          </h1>
          <p className="mt-3 max-w-3xl text-slate-700">
            Upload a resume PDF, extract skills using NLP, compare it to a job description with cosine
            similarity, and receive actionable improvements powered by an LLM.
          </p>
        </header>

        <div className="grid gap-6 lg:grid-cols-2">
          <Panel
            title="Resume Intake"
            subtitle="Upload a PDF or choose a previous resume to analyze against a target role."
          >
            <form className="space-y-4" onSubmit={handleUpload}>
              <label className="block">
                <span className="mb-2 block text-sm font-medium text-slate-700">Upload resume PDF</span>
                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={(event) => setResumeFile(event.target.files?.[0] || null)}
                  className="block w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm file:mr-4 file:rounded-lg file:border-0 file:bg-teal-700 file:px-3 file:py-2 file:text-sm file:font-semibold file:text-white hover:file:bg-teal-800"
                />
              </label>

              <button
                type="submit"
                disabled={loadingUpload}
                className="w-full rounded-xl bg-teal-700 px-4 py-2.5 font-semibold text-white transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:bg-slate-400"
              >
                {loadingUpload ? "Uploading and extracting..." : "Upload and Extract Skills"}
              </button>
            </form>

            <div className="mt-4 rounded-2xl border border-slate-200 bg-white p-4">
              <label className="block">
                <span className="mb-2 block text-sm font-medium text-slate-700">Or select existing resume</span>
                <select
                  className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm"
                  value={selectedResumeId}
                  onChange={(event) => {
                    setSelectedResumeId(event.target.value);
                    setUploadedResume(null);
                  }}
                >
                  <option value="">Select a resume</option>
                  {resumes.map((resume) => (
                    <option key={resume.id} value={resume.id}>
                      {resume.filename} | {new Date(resume.created_at).toLocaleString()}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            {uploadedResume && (
              <div className="mt-4 rounded-2xl border border-emerald-300 bg-emerald-50 p-4">
                <p className="text-sm font-semibold text-emerald-900">Latest extracted skills</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {uploadedResume.extracted_skills.length > 0 ? (
                    uploadedResume.extracted_skills.map((skill) => <SkillPill key={skill} label={skill} />)
                  ) : (
                    <p className="text-sm text-slate-600">No skills detected from this resume.</p>
                  )}
                </div>
              </div>
            )}
          </Panel>

          <Panel
            title="Target Job"
            subtitle="Paste a job description and run match scoring with AI feedback."
          >
            <form className="space-y-4" onSubmit={handleAnalyze}>
              <label className="block">
                <span className="mb-2 block text-sm font-medium text-slate-700">Job title</span>
                <input
                  value={jobTitle}
                  onChange={(event) => setJobTitle(event.target.value)}
                  placeholder="Senior Backend Engineer"
                  className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2"
                />
              </label>

              <label className="block">
                <span className="mb-2 block text-sm font-medium text-slate-700">Job description</span>
                <textarea
                  value={jobDescription}
                  onChange={(event) => setJobDescription(event.target.value)}
                  rows={10}
                  className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2"
                />
              </label>

              <button
                type="submit"
                disabled={loadingMatch}
                className="w-full rounded-xl bg-orange-600 px-4 py-2.5 font-semibold text-white transition hover:bg-orange-700 disabled:cursor-not-allowed disabled:bg-slate-400"
              >
                {loadingMatch ? "Running AI analysis..." : "Analyze Match"}
              </button>
            </form>
          </Panel>
        </div>

        {error && (
          <div className="rounded-2xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-800">{error}</div>
        )}

        {analysis && (
          <section className="grid gap-6 lg:grid-cols-[280px_1fr]">
            <div className="rounded-3xl border border-white/80 bg-white/75 p-5 shadow-glow backdrop-blur-md">
              <p className="text-sm uppercase tracking-wider text-slate-500">Skill Match</p>
              <div className="mt-4 flex items-center justify-center">
                <div className="relative h-44 w-44 rounded-full p-3" style={scoreStyle}>
                  <div className="flex h-full w-full items-center justify-center rounded-full bg-white text-center shadow-inner">
                    <div>
                      <p className="text-5xl font-bold text-teal-800">{score}%</p>
                      <p className="text-sm text-slate-500">overall fit</p>
                    </div>
                  </div>
                </div>
              </div>
              <p className="mt-4 text-sm text-slate-600">
                Resume ID: {analysis.resume_id} {analysis.job_title ? `| Role: ${analysis.job_title}` : ""}
              </p>
            </div>

            <div className="space-y-4">
              <div className="rounded-3xl border border-white/80 bg-white/75 p-5 shadow-glow backdrop-blur-md">
                <h3 className="text-lg font-semibold">Matched skills</h3>
                <div className="mt-3 flex flex-wrap gap-2">
                  {analysis.matched_skills.length > 0 ? (
                    analysis.matched_skills.map((skill) => (
                      <SkillPill key={skill} label={skill} tone="good" />
                    ))
                  ) : (
                    <p className="text-sm text-slate-600">No direct skill matches found.</p>
                  )}
                </div>
              </div>

              <div className="rounded-3xl border border-white/80 bg-white/75 p-5 shadow-glow backdrop-blur-md">
                <h3 className="text-lg font-semibold">Skill gaps</h3>
                <div className="mt-3 flex flex-wrap gap-2">
                  {analysis.missing_skills.length > 0 ? (
                    analysis.missing_skills.map((skill) => (
                      <SkillPill key={skill} label={skill} tone="gap" />
                    ))
                  ) : (
                    <p className="text-sm text-slate-600">No missing skills detected from the parsed job text.</p>
                  )}
                </div>
              </div>

              <div className="rounded-3xl border border-white/80 bg-white/75 p-5 shadow-glow backdrop-blur-md">
                <h3 className="text-lg font-semibold">Resume improvement suggestions</h3>
                <ol className="mt-3 space-y-2 text-sm text-slate-700">
                  {analysis.suggestions.map((suggestion, index) => (
                    <li key={`${suggestion}-${index}`} className="rounded-xl border border-slate-200 bg-white px-3 py-2">
                      {index + 1}. {suggestion}
                    </li>
                  ))}
                </ol>
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}
