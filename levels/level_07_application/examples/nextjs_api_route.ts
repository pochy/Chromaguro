import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL = process.env.RAG_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const q = searchParams.get("q");

  if (!q) {
    return NextResponse.json({ error: "q is required" }, { status: 400 });
  }

  const tenantId = searchParams.get("tenant_id") ?? "tenant_a";
  const docType = searchParams.get("doc_type");

  const upstream = new URL("/search", API_BASE_URL);
  upstream.searchParams.set("q", q);
  upstream.searchParams.set("tenant_id", tenantId);
  if (docType) {
    upstream.searchParams.set("doc_type", docType);
  }

  const response = await fetch(upstream, { cache: "no-store" });

  if (!response.ok) {
    return NextResponse.json({ error: "search failed" }, { status: response.status });
  }

  return NextResponse.json(await response.json());
}

