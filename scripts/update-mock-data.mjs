/**
 * Fetch GA4 data and patch src/lib/mock-data.ts in place.
 * Only the ga4 export and PERIOD line are rewritten; everything else stays.
 *
 * Run locally:  node scripts/update-mock-data.mjs
 * CI:           GA4_PRIVATE_KEY="..." node scripts/update-mock-data.mjs
 */
import { google } from "googleapis";
import { readFileSync, writeFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const MOCK_DATA_PATH = resolve(__dirname, "../src/lib/mock-data.ts");

const GA4_PROPERTY = "properties/542631495";

// SA credentials — env var overrides hardcoded key (for CI)
const SA_PRIVATE_KEY =
  process.env.GA4_PRIVATE_KEY ||
  `-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCsCZiLiK4WH7ms
Oh/Ix7fCbEYy9OY+tzUhCJvjFVNdJv7f4ScJ5peR0oYRIzG3IZ/asrbQS/o+D/uN
pbC+4WDLQIJVSqMZkQPgWNVHsvwzxoxfA7g0rIBBQaue5a/2ms/x2fTQAhZ9Whc+
sjkC6EgeP85PXke6E/TXleRb6pQkJHPc/VAltH1QY6qKPNyDGyk/L/H44GClInDB
qYi1nH6mtfwdH0YwsDOf84DiQXfxlesVYvtlf3gwzuLqmoVOeIEXHq5Vi/Gue8MD
8jBk5SYdmuAHCtIhkN5zXN47r7ObyeTzoBPDPXnaKP9C/3wjDJ/CaiAUOebYS5UI
KawpeogfAgMBAAECggEABoq4El8O4G6xzklIvSDorXJIxxZF84H4kyCzLZ+5eec9
aOdnmlPg7p224f7yT7iHgVCR00dLi3TRh+TfKc42ZcEDU7/3UyxCNy0//i57TAxT
eSd4jgdpoLgHd47cMc0lD1k056+bCe0IYw0LtIvlqVs1Ld9An5eAeq3Llbn/veui
H9+/i1mt5rFW0+DSOWMBfcYmqSmL/yxMWrZ90n79PomES1SeJI04qEEqunNK8boB
uIPDdTh1x+YubC0aG+EWhpNLTHovU7BCPoZeWRyB086t/9/iF5hPfQDGrbhZ9Y4U
ifVaIxe3Ge06I0f5zC5a/C04xH5I4pQUGg6SOHn40QKBgQDjfb+erxYVSlMHSEV6
qfg/x8DVygTLUFaUSzXBYXwl5drP7FTTh6zbMG+LLf+thPpX8ZAd3C234Fy9bbRE
jeQD/koXdr1/BWcKm/joceG5XrFbhyXvc72Eq3a9ZqfXNbDfeDnhZ3v+dLtR29Na
1wcmqDO08X6vlNZbHBnlISCmDwKBgQDBmM+HiqXMFzIAJlazPG/qpmKVmice9ang
h4p6JyRejfhqQyA8Z3p8Ct0It3hZKxryy34PCoEDwdOxBek2gzZxmxqOx1CkAHhh
YSlrqy7CpIA+pCr89+5MDjJxumljygjShtK3J/zLu5nnaSdQgNuDdsmL4fqG+0mP
YAUbUDKM8QKBgQDXiHBgW+pESaLYp3SMfzUg2JSu+TQJnRgqcAeCLGZ/UYM6s+K6
dzUihoVoDDDNqcu2PrwYTl9Sc1PqdWHyAa0iy25PRMTM78Vsm9H8CMmf40OOQEGE
2NeaNwnM8NHcaJYnY7UTBgTIVLiVGfzpeAjia0JyEMvCdvWQZNNz7ysLqQKBgQCE
KNBLZC/o0lDU31dChliUZD9ah2B7dxMf7wduejgOwHY7/FUOR0nLUhMwNydWH+IG
qzoEBJSsPu5Ho5RgHVTWWx7XJ2N6gcOsHosLMFH8mBXgLWwXQx2PGAYBs1Lsx2gc
Z+ODGy4s2oWm/xbSkxTHexj9gCfpa7P8x3zU93t60QKBgF96C9dFmt3CW7zhIoft
GFv1DdXwXqoVpsNgcHhPlIOMwsOYYxG8GzgbFzTpsMiHFVJ746XxxT4TqMR1mmOq
lRRKvqwclmJHD5Sf5Oq5n+GzdNrwo3dCrDRyYsTLLmSLWnECivk9avV5DT915Uj3
ZLQQfUcwIsgUituz9ikeUDAU
-----END PRIVATE KEY-----
`;

const SA = {
  type: "service_account",
  project_id: "perfect-trilogy-467812-p4",
  private_key_id: "23697a08ed01149d1c39e1a7a08f50a76c81d3ba",
  private_key: SA_PRIVATE_KEY,
  client_email:
    "atelier-service-account@perfect-trilogy-467812-p4.iam.gserviceaccount.com",
  client_id: "113524929199575319905",
};

function fmtDate(d) {
  return `${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

function fmtEngagement(totalSeconds, sessionCount) {
  if (!sessionCount) return '"—"';
  const avg = Math.round(totalSeconds / sessionCount);
  const m = Math.floor(avg / 60);
  const s = String(avg % 60).padStart(2, "0");
  return `"${m}m ${s}s"`;
}

async function main() {
  const auth = new google.auth.GoogleAuth({
    credentials: SA,
    scopes: ["https://www.googleapis.com/auth/analytics.readonly"],
  });
  const api = google.analyticsdata({ version: "v1beta", auth });

  console.log("Fetching GA4 data...");

  // Current period (30 days)
  const [daily, prev, sources, landing] = await Promise.all([
    api.properties.runReport({
      property: GA4_PROPERTY,
      requestBody: {
        dateRanges: [{ startDate: "30daysAgo", endDate: "today" }],
        dimensions: [{ name: "date" }],
        metrics: [
          { name: "sessions" },
          { name: "totalUsers" },
          { name: "newUsers" },
          { name: "userEngagementDuration" },
        ],
        orderBys: [{ dimension: { dimensionName: "date" } }],
        dimensionFilter: {
          filter: {
            fieldName: "hostName",
            stringFilter: {
              value: "good-genes-clinic.com",
              matchType: "EXACT"
            }
          }
        }
      },
    }),
    api.properties.runReport({
      property: GA4_PROPERTY,
      requestBody: {
        dateRanges: [{ startDate: "60daysAgo", endDate: "31daysAgo" }],
        metrics: [
          { name: "sessions" },
          { name: "totalUsers" },
          { name: "userEngagementDuration" },
        ],
        dimensionFilter: {
          filter: {
            fieldName: "hostName",
            stringFilter: {
              value: "good-genes-clinic.com",
              matchType: "EXACT"
            }
          }
        }
      },
    }),
    api.properties.runReport({
      property: GA4_PROPERTY,
      requestBody: {
        dateRanges: [{ startDate: "30daysAgo", endDate: "today" }],
        dimensions: [{ name: "sessionDefaultChannelGroup" }],
        metrics: [{ name: "sessions" }],
        orderBys: [{ metric: { metricName: "sessions" }, desc: true }],
        dimensionFilter: {
          filter: {
            fieldName: "hostName",
            stringFilter: {
              value: "good-genes-clinic.com",
              matchType: "EXACT"
            }
          }
        }
      },
    }),
    api.properties.runReport({
      property: GA4_PROPERTY,
      requestBody: {
        dateRanges: [{ startDate: "30daysAgo", endDate: "today" }],
        dimensions: [{ name: "landingPagePlusQueryString" }],
        metrics: [{ name: "sessions" }, { name: "userEngagementDuration" }],
        orderBys: [{ metric: { metricName: "sessions" }, desc: true }],
        limit: 10,
        dimensionFilter: {
          filter: {
            fieldName: "hostName",
            stringFilter: {
              value: "good-genes-clinic.com",
              matchType: "EXACT"
            }
          }
        }
      },
    }),
  ]);

  // Aggregate current period
  const rows = daily.data.rows || [];
  let totalSessions = 0, totalUsers = 0, totalEngagement = 0;
  const trendEntries = [];
  for (const r of rows) {
    const d = r.dimensionValues[0].value; // "20260624"
    const sessions = +r.metricValues[0].value;
    const users = +r.metricValues[1].value;
    const eng = +r.metricValues[3].value;
    totalSessions += sessions;
    totalUsers += users;
    totalEngagement += eng;
    const mm = d.slice(4, 6);
    const dd = d.slice(6, 8);
    trendEntries.push(`    { day: "${mm}-${dd}", value: ${sessions} }`);
  }

  // Previous period for deltas
  const prevRows = prev.data.rows || [];
  let prevSessions = 0, prevUsers = 0;
  for (const r of prevRows) {
    prevSessions += +r.metricValues[0].value;
    prevUsers += +r.metricValues[1].value;
  }
  const sessionsDelta = prevSessions ? ((totalSessions - prevSessions) / prevSessions) : 0;
  const usersDelta = prevUsers ? ((totalUsers - prevUsers) / prevUsers) : 0;

  // Sources
  const srcRows = sources.data.rows || [];
  const srcTotal = srcRows.reduce((s, r) => s + +r.metricValues[0].value, 0) || 1;
  const sourceEntries = srcRows.map((r) => {
    const name = r.dimensionValues[0].value;
    const val = +r.metricValues[0].value;
    return `    { name: "${name}", value: ${val}, share: ${(val / srcTotal).toFixed(2)} }`;
  });

  // Landing pages
  const landRows = (landing.data.rows || []).slice(0, 8);
  const landEntries = landRows.map((r) => {
    const path = r.dimensionValues[0].value || "/";
    const sess = +r.metricValues[0].value;
    const eng = +r.metricValues[1].value;
    const avgSec = sess ? Math.round(eng / sess) : 0;
    const m = Math.floor(avgSec / 60);
    const s = String(avgSec % 60).padStart(2, "0");
    return `    { path: "${path}", sessions: ${sess}, time: "${m}m ${s}s" }`;
  });

  // Date range for PERIOD
  const today = new Date();
  const thirtyAgo = new Date(today);
  thirtyAgo.setDate(thirtyAgo.getDate() - 30);
  const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  const periodStr = `Last 30 days · ${thirtyAgo.getDate()} ${months[thirtyAgo.getMonth()]} – ${today.getDate()} ${months[today.getMonth()]} ${today.getFullYear()}`;

  const engStr = fmtEngagement(totalEngagement, totalSessions);
  const pullDate = `${today.getDate()} ${months[today.getMonth()]} ${today.getFullYear()}`;

  // Build GA4 block
  const ga4Block = `// 1. GA4 — LIVE DATA · property 542631495 · pulled ${pullDate}
export const ga4 = {
  sessions: ${totalSessions},
  sessionsDelta: ${sessionsDelta.toFixed(3)},
  users: ${totalUsers},
  usersDelta: ${usersDelta.toFixed(3)},
  engagementTime: ${engStr},
  engagementDelta: 0,
  inquiries: 0,
  inquiriesDelta: 0,
  sessionsTrend: [
${trendEntries.join(",\n")}${trendEntries.length ? "," : ""}
  ],
  sources: [
${sourceEntries.join(",\n")}${sourceEntries.length ? "," : ""}
  ],
  landing: [
${landEntries.join(",\n")}${landEntries.length ? "," : ""}
  ],
};`;

  // Read, patch, write
  let src = readFileSync(MOCK_DATA_PATH, "utf-8");

  // Replace PERIOD line
  src = src.replace(
    /export const PERIOD = ".*?";/,
    `export const PERIOD = "${periodStr}";`,
  );

  // Replace GA4 block (from comment to closing };)
  src = src.replace(
    /\/\/ 1\. GA4[^\n]*\n[\s\S]*?^};/m,
    ga4Block,
  );

  writeFileSync(MOCK_DATA_PATH, src);
  console.log(`Updated mock-data.ts — ${totalSessions} sessions, ${totalUsers} users (${periodStr})`);
}

main().catch((err) => {
  console.error("FATAL:", err.message);
  process.exit(1);
});
