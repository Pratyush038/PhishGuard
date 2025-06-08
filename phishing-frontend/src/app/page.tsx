"use client";

import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Terminal, Loader2, Info } from "lucide-react";
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";

export default function PhishingDetection() {
  const [url, setUrl] = useState("");
  const [prediction, setPrediction] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!url.trim()) {
      alert("Please enter a URL.");
      return;
    }
    try {
      setLoading(true);
      const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL;
      const res = await fetch(`${apiBase}/predict_from_url`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await res.json();
      setPrediction(data.prediction);
    } catch (error) {
      alert("Error while making prediction: " + (error as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="flex flex-col items-center justify-center min-h-screen p-8"
      style={{
        backgroundColor: "#000",
        backgroundImage:
          "radial-gradient(circle, grey 0.4px, transparent 0.2px)",
        backgroundSize: "20px 20px",
      }}
    >
      <Card
        className="w-full max-w-xl rounded-2xl shadow-xl border border-white/40"
        style={{
          backgroundColor: "rgba(255, 255, 255, 0.9)",
          backdropFilter: "blur(10px)",
          WebkitBackdropFilter: "blur(10px)", // for Safari
          border: "1px solid rgba(255, 255, 255, 0.3)",
          color: "#111", // dark text on white card
        }}
      >
        <CardContent className="pt-4 px-8 pb-8">
          <div className="flex justify-between items-start mb-10">
            <div className="flex-1 text-center">
              <h2 className="text-6xl md:text-2xl lg:text-3xl font-bold tracking-tight text-[#111] leading-snug">
                PhishGuard
                <span className="block text-base md:text-lg font-medium italic text-gray-600">
                  AI that spots phishing, so you don&apos;t have to.
                </span>
              </h2>
            </div>
            <Dialog>
              <DialogTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  className="text-neutral-600 hover:text-black"
                  aria-label="About this app"
                >
                  <Info className="h-6 w-6" />
                </Button>
              </DialogTrigger>
              <DialogContent
                className="max-w-lg rounded-2xl"
                style={{ backgroundColor: "#fff", color: "#111" }}
              >
                <DialogHeader>
                  <DialogTitle
                    className="text-xl font-bold"
                    style={{ color: "black" }}
                  >
                    About This App
                  </DialogTitle>
                  <DialogDescription className="mt-2 text-sm leading-relaxed text-gray-800">
                    This phishing detection system is powered by machine learning
                    models trained on a dataset of approximately 11,000 URLs,
                    labeled as either phishing or legitimate. The system uses two
                    models — XGBoost and RandomForestClassifier — currently using
                    XGBoost for improved accuracy and can be switched with
                    RandomForestClassifier for improved speed.
                    <br />
                    <br />
                    Each URL is parsed to extract 30 handcrafted features,
                    including indicators such as the presence of an IP address,
                    use of the &apos;@&apos; symbol, number of subdomains, URL length,
                    HTTPS usage, and more.
                    <br />
                    <br />
                    Once you submit a URL, these features are computed on the
                    backend. The FastAPI server then uses the trained ML model to
                    classify the URL as either Safe ✅ or Phishing ⚠️, and sends
                    the result back to the frontend.
                    <br />
                    <br />
                    This user interface is built with Next.js and ShadCN UI,
                    offering a clean, responsive, and modern experience to help
                    users assess the safety of URLs with just one click.
                  </DialogDescription>
                </DialogHeader>
              </DialogContent>
            </Dialog>
          </div>

          <p className="mb-4 text-center text-gray-600">
            Enter a URL below to check if it might be a phishing site.
          </p>

          <Label
            htmlFor="url"
            className="mb-3 block text-sm font-semibold"
            style={{ color: "#222" }}
          >
            Website URL:
          </Label>
          <Input
            id="url"
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            className="mb-8 border border-gray-400 focus:ring-gray-600 focus:border-gray-600"
            style={{
              backgroundColor: "#f9f9f9",
              color: "#111",
              borderRadius: "6px",
              padding: "0.5rem 1rem",
            }}
          />

          <div className="flex gap-5">
            <Button
              onClick={handleSubmit}
              disabled={loading}
              className="bg-black hover:bg-gray-900 text-white shadow-md rounded-md transition-colors duration-300"
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin mr-2 h-5 w-5" /> Detecting...
                </>
              ) : (
                "Detect"
              )}
            </Button>
            <Button
              variant="outline"
              onClick={() => {
                setUrl("");
                setPrediction(null);
              }}
              disabled={loading}
              className="border border-black text-black hover:bg-black hover:text-white rounded-md transition-colors duration-300"
            >
              Clear
            </Button>
          </div>

          {prediction !== null && (
            <Alert
              variant={prediction === 1 ? "destructive" : "default"}
              className={`mt-10 flex items-center space-x-4 rounded-md px-6 py-5 ${
                prediction === 1
                  ? "bg-red-100 border border-red-400 text-red-800 shadow"
                  : "bg-green-100 border border-green-400 text-green-800 shadow"
              }`}
            >
              <Terminal
                className={`h-6 w-6 ${
                  prediction === 1 ? "text-red-700" : "text-green-700"
                }`}
              />
              <div>
                <AlertTitle className="text-lg font-semibold text-black">
                  Prediction Result
                </AlertTitle>
                <AlertDescription className="text-sm text-black">
                  This website is predicted to be:{" "}
                  <strong>{prediction === 1 ? "Phishing ⚠️" : "Safe ✅"}</strong>
                </AlertDescription>
              </div>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Footer Card below main Card */}
      <Card
        className="w-full max-w-xl rounded-2xl shadow-md border border-white/30 mt-8"
        style={{
          backgroundColor: "rgba(255, 255, 255, 0.8)",
          backdropFilter: "blur(8px)",
          WebkitBackdropFilter: "blur(8px)", // Safari support
          border: "1px solid rgba(255, 255, 255, 0.2)",
          color: "#111",
        }}
      >
        <CardContent className="flex flex-col sm:flex-row items-center justify-between gap-4 text-sm px-6 py-3">
          <div className="text-center sm:text-left text-gray-700 flex items-center justify-center sm:justify-start">
            <span>Made with ❤️ by Pratyush</span>
          </div>
          <div className="flex items-center space-x-4 justify-center sm:justify-end text-gray-700">
            <a
              href="https://github.com/Pratyush038"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:opacity-80 opacity-70 transition-opacity flex items-center space-x-1"
              aria-label="GitHub Repository"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                fill="currentColor"
                viewBox="0 0 24 24"
                style={{ color: "#111" }}
              >
                <path d="M12 .5C5.37.5 0 5.87 0 12.45c0 5.28 3.44 9.75 8.2 11.33.6.11.82-.26.82-.58 0-.29-.01-1.05-.02-2.05-3.34.74-4.04-1.61-4.04-1.61-.55-1.41-1.34-1.78-1.34-1.78-1.1-.76.09-.75.09-.75 1.22.09 1.87 1.29 1.87 1.29 1.08 1.88 2.83 1.34 3.52 1.03.11-.8.42-1.34.76-1.65-2.67-.31-5.47-1.36-5.47-6.06 0-1.34.47-2.43 1.24-3.29-.12-.31-.54-1.57.12-3.28 0 0 1.01-.33 3.3 1.26a11.37 11.37 0 013.01-.41c1.02.01 2.05.14 3.01.41 2.29-1.6 3.3-1.26 3.3-1.26.66 1.71.24 2.97.12 3.28.77.86 1.24 1.95 1.24 3.29 0 4.71-2.81 5.75-5.49 6.06.43.37.82 1.1.82 2.22 0 1.6-.02 2.88-.02 3.27 0 .32.22.69.83.57C20.56 22.2 24 17.73 24 12.45 24 5.87 18.63.5 12 .5z" />
              </svg>
              <span>GitHub</span>
            </a>
            <a
              href="https://www.linkedin.com/in/pratyushbidare/"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="LinkedIn Profile"
              className="hover:opacity-80 opacity-70 transition-opacity flex items-center"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                fill="currentColor"
                viewBox="0 0 24 24"
                style={{ color: "#111" }}
              >
                <path d="M20.447 20.452H16.9v-5.569c0-1.327-.026-3.037-1.852-3.037-1.853 0-2.136 1.447-2.136 2.942v5.664H9.365V9h3.413v1.561h.05c.476-.9 1.637-1.852 3.37-1.852 3.605 0 4.27 2.372 4.27 5.458v6.285zM5.337 7.433a1.98 1.98 0 110-3.959 1.98 1.98 0 010 3.959zm1.725 13.019H3.61V9h3.452v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.73v20.54C0 23.23.792 24 1.771 24h20.451C23.2 24 24 23.23 24 22.27V1.73C24 .774 23.2 0 22.225 0z" />
              </svg>
            </a>
          </div>
        </CardContent>
      </Card>

    </div>
  );
}
