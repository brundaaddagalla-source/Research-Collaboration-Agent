import { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import { Radar, Loader2 } from "lucide-react";

import { requestFacultyGrid, facultyLogin } from "../services/api";

import { setStoredFaculty, isAuthenticated } from "../services/auth";

export default function FacultyLogin() {
  const navigate = useNavigate();

  const [facultyId, setFacultyId] = useState("");
  const [password, setPassword] = useState("");
  const [gridPositions, setGridPositions] = useState(["", ""]);
  const [gridValues, setGridValues] = useState(["", ""]);
  const [gridRequested, setGridRequested] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (isAuthenticated()) {
      navigate("/", { replace: true });
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const idError =
    facultyId.length > 0 && !/^\d{5}$/.test(facultyId)
      ? "Faculty ID must be exactly 5 digits."
      : "";

  function handleFacultyIdChange(event) {
    const digitsOnly = event.target.value
      .replace(/\D/g, "")
      .slice(0, 5);

    setFacultyId(digitsOnly);
    setError("");

    // Reset grid if Faculty ID changes
    setGridRequested(false);
    setGridPositions(["", ""]);
    setGridValues(["", ""]);
    setPassword("");

    // Automatically request grid when 5 digits are entered
    if (digitsOnly.length === 5) {
      handleRequestGrid(digitsOnly);
    }
  }

  async function handleRequestGrid(id) {
    if (!/^\d{5}$/.test(id)) {
      setError("Please enter a valid 5-digit Faculty ID.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const result = await requestFacultyGrid(id.trim());

      setGridPositions(result.gridPositions);
      setGridRequested(true);
    } catch (err) {
      setGridPositions(["", ""]);
      setGridRequested(false);

      setError(
        err.message ||
          "Could not verify Faculty ID. Please check the ID and try again."
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleLogin(event) {
    event.preventDefault();
    setError("");

    if (!/^\d{5}$/.test(facultyId)) {
      setError("Please enter a valid 5-digit Faculty ID.");
      return;
    }

    if (!gridRequested) {
      setError("Please wait for the grid positions to load.");
      return;
    }

    if (
      !password ||
      !gridValues[0].trim() ||
      !gridValues[1].trim()
    ) {
      setError("Please fill in your password and both grid values.");
      return;
    }

    setLoading(true);

    try {
      const result = await facultyLogin({
        facultyId: facultyId.trim(),
        password,
        gridValues,
      });

      setStoredFaculty({
        ...result.faculty,
        loginAt: new Date().toISOString(),
      });

      navigate("/", { replace: true });
    } catch (err) {
      setError(
        err.message ||
          "Login failed. Please check your details and try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-sky-50 px-4 py-6">
      <div className="w-full max-w-[440px] rounded-panel border border-surface-line bg-white p-8 shadow-panel sm:p-10">
        {/* Brand */}
        <div className="mb-7 flex flex-col items-center text-center">
          <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-soft-blue ring-1 ring-blue/10">
            <Radar className="h-6 w-6 text-accent-blue" />
          </div>

          <h1 className="font-display text-2xl font-bold text-navy-800">
            Agent 24
          </h1>

          <p className="mt-1 text-sm text-surface-muted">
            Research Collaboration Platform
          </p>
        </div>

        <form onSubmit={handleLogin} className="space-y-5">
          {/* Faculty ID */}
          <div>
            <label
              htmlFor="facultyId"
              className="mb-1.5 block text-sm font-medium text-navy-800"
            >
              Faculty ID
            </label>

            <input
              id="facultyId"
              type="text"
              inputMode="numeric"
              pattern="\d{5}"
              maxLength={5}
              value={facultyId}
              onChange={handleFacultyIdChange}
              placeholder="e.g. 10243"
              autoFocus
              className={`w-full rounded-lg border bg-white px-3.5 py-2.5 text-sm text-navy-800 outline-none transition focus:ring-2 ${
                idError
                  ? "border-signal-dormant focus:border-signal-dormant focus:ring-signal-dormant/15"
                  : "border-surface-line focus:border-accent-blue focus:ring-accent-blue/15"
              }`}
            />

            {idError && (
              <p className="mt-1.5 text-xs text-signal-dormant">
                {idError}
              </p>
            )}

            {/* Loading indicator after 5-digit Faculty ID */}
            {loading && facultyId.length === 5 && !gridRequested && (
              <div className="mt-2 flex items-center gap-2 text-xs text-surface-muted">
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                Loading grid positions...
              </div>
            )}
          </div>

          {/* Password */}
          <div>
            <label
              htmlFor="password"
              className="mb-1.5 block text-sm font-medium text-navy-800"
            >
              Password
            </label>

            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setError("");
              }}
              placeholder="Enter Password"
              className="w-full rounded-lg border border-surface-line bg-white px-3.5 py-2.5 text-sm text-navy-800 outline-none transition focus:border-accent-blue focus:ring-2 focus:ring-accent-blue/15"
            />
          </div>

          {/* Grid Values */}
          <div className="grid grid-cols-2 gap-4">
            {/* Grid 1 */}
            <div>
              <label
                htmlFor="grid1"
                className="mb-1.5 block text-sm font-medium text-navy-800"
              >
                Grid Value{" "}
                {gridPositions[0] && (
                  <span className="font-bold text-accent-blue">
                    {gridPositions[0]}
                  </span>
                )}
              </label>

              <input
                id="grid1"
                type="password"
                value={gridValues[0]}
                onChange={(e) =>
                  setGridValues([
                    e.target.value,
                    gridValues[1],
                  ])
                }
                placeholder={
                  gridPositions[0]
                    ? `Enter ${gridPositions[0]}`
                    : "Enter grid value"
                }
                className="w-full rounded-lg border border-surface-line bg-white px-3.5 py-2.5 text-sm text-navy-800 outline-none transition focus:border-accent-blue focus:ring-2 focus:ring-accent-blue/15"
              />
            </div>

            {/* Grid 2 */}
            <div>
              <label
                htmlFor="grid2"
                className="mb-1.5 block text-sm font-medium text-navy-800"
              >
                Grid Value{" "}
                {gridPositions[1] && (
                  <span className="font-bold text-accent-blue">
                    {gridPositions[1]}
                  </span>
                )}
              </label>

              <input
                id="grid2"
                type="password"
                value={gridValues[1]}
                onChange={(e) =>
                  setGridValues([
                    gridValues[0],
                    e.target.value,
                  ])
                }
                placeholder={
                  gridPositions[1]
                    ? `Enter ${gridPositions[1]}`
                    : "Enter grid value"
                }
                className="w-full rounded-lg border border-surface-line bg-white px-3.5 py-2.5 text-sm text-navy-800 outline-none transition focus:border-accent-blue focus:ring-2 focus:ring-accent-blue/15"
              />
            </div>
          </div>

          {/* Error */}
          {error && (
            <p className="rounded-lg bg-signal-dormant/5 px-3 py-2 text-xs text-signal-dormant">
              {error}
            </p>
          )}

          {/* Login */}
          <button
            type="submit"
            disabled={loading || !gridRequested}
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-accent-blue px-4 py-2.5 text-sm font-medium text-white transition hover:bg-navy-700 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {loading && (
              <Loader2 className="h-4 w-4 animate-spin" />
            )}

            Login
          </button>
        </form>
      </div>
    </div>
  );
}
