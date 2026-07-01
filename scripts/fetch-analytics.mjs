/**
 * Fetch real analytics data from GA4 + Search Console.
 * Run: node scripts/fetch-analytics.mjs
 */
import { google } from 'googleapis';

const SA = {
  type: 'service_account',
  project_id: 'perfect-trilogy-467812-p4',
  private_key_id: '23697a08ed01149d1c39e1a7a08f50a76c81d3ba',
  private_key: `-----BEGIN PRIVATE KEY-----
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
`,
  client_email: 'atelier-service-account@perfect-trilogy-467812-p4.iam.gserviceaccount.com',
  client_id: '113524929199575319905',
  auth_uri: 'https://accounts.google.com/o/oauth2/auth',
  token_uri: 'https://oauth2.googleapis.com/token',
};

const GA4_PROPERTY = 'properties/542631495';

async function main() {
  const auth = new google.auth.GoogleAuth({
    credentials: SA,
    scopes: [
      'https://www.googleapis.com/auth/analytics.readonly',
      'https://www.googleapis.com/auth/webmasters.readonly',
    ],
  });

  const analyticsdata = google.analyticsdata({ version: 'v1beta', auth });

  // ── GA4: daily sessions/users/engagement ──────────────────────────────────
  const daily = await analyticsdata.properties.runReport({
    property: GA4_PROPERTY,
    requestBody: {
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      dimensions: [{ name: 'date' }],
      metrics: [
        { name: 'sessions' },
        { name: 'totalUsers' },
        { name: 'newUsers' },
        { name: 'userEngagementDuration' },
      ],
      orderBys: [{ dimension: { dimensionName: 'date' } }],
      dimensionFilter: {
        filter: {
          fieldName: 'hostName',
          stringFilter: {
            value: 'good-genes-clinic.com',
            matchType: 'EXACT'
          }
        }
      }
    },
  });

  // ── GA4: previous 30 days (for deltas) ────────────────────────────────────
  const prevPeriod = await analyticsdata.properties.runReport({
    property: GA4_PROPERTY,
    requestBody: {
      dateRanges: [{ startDate: '60daysAgo', endDate: '31daysAgo' }],
      metrics: [
        { name: 'sessions' },
        { name: 'totalUsers' },
        { name: 'userEngagementDuration' },
      ],
      dimensionFilter: {
        filter: {
          fieldName: 'hostName',
          stringFilter: {
            value: 'good-genes-clinic.com',
            matchType: 'EXACT'
          }
        }
      }
    },
  });

  // ── GA4: traffic sources (channel group) ──────────────────────────────────
  const sources = await analyticsdata.properties.runReport({
    property: GA4_PROPERTY,
    requestBody: {
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      dimensions: [{ name: 'sessionDefaultChannelGroup' }],
      metrics: [{ name: 'sessions' }],
      orderBys: [{ metric: { metricName: 'sessions' }, desc: true }],
      dimensionFilter: {
        filter: {
          fieldName: 'hostName',
          stringFilter: {
            value: 'good-genes-clinic.com',
            matchType: 'EXACT'
          }
        }
      }
    },
  });

  // ── GA4: landing pages ────────────────────────────────────────────────────
  const landing = await analyticsdata.properties.runReport({
    property: GA4_PROPERTY,
    requestBody: {
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      dimensions: [{ name: 'landingPagePlusQueryString' }],
      metrics: [{ name: 'sessions' }, { name: 'userEngagementDuration' }],
      orderBys: [{ metric: { metricName: 'sessions' }, desc: true }],
      limit: 10,
      dimensionFilter: {
        filter: {
          fieldName: 'hostName',
          stringFilter: {
            value: 'good-genes-clinic.com',
            matchType: 'EXACT'
          }
        }
      }
    },
  });

  // ── GA4: new vs returning ─────────────────────────────────────────────────
  const newVsReturning = await analyticsdata.properties.runReport({
    property: GA4_PROPERTY,
    requestBody: {
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      dimensions: [{ name: 'newVsReturning' }],
      metrics: [{ name: 'totalUsers' }, { name: 'sessions' }],
      dimensionFilter: {
        filter: {
          fieldName: 'hostName',
          stringFilter: {
            value: 'good-genes-clinic.com',
            matchType: 'EXACT'
          }
        }
      }
    },
  });

  // ── GA4: key events (form_submit / contact / inquiry) ────────────────────
  const events = await analyticsdata.properties.runReport({
    property: GA4_PROPERTY,
    requestBody: {
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      dimensions: [{ name: 'eventName' }],
      metrics: [{ name: 'eventCount' }],
      orderBys: [{ metric: { metricName: 'eventCount' }, desc: true }],
      limit: 30,
      dimensionFilter: {
        filter: {
          fieldName: 'hostName',
          stringFilter: {
            value: 'good-genes-clinic.com',
            matchType: 'EXACT'
          }
        }
      }
    },
  });

  // ── Search Console: list verified sites ───────────────────────────────────
  const sc = google.searchconsole({ version: 'v1', auth });
  let scSites = null;
  try {
    const sitesRes = await sc.sites.list();
    scSites = sitesRes.data;
  } catch (e) {
    scSites = { error: e.message };
  }

  // ── Search Console: query data (try both URL formats) ────────────────────
  const siteUrlsToTry = [
    'https://good-genes.com/',
    'sc-domain:good-genes.com',
  ];

  let scOverall = null;
  let scQueries = null;
  let scPages = null;
  let usedSiteUrl = null;

  for (const siteUrl of siteUrlsToTry) {
    try {
      const overall = await sc.searchanalytics.query({
        siteUrl,
        requestBody: {
          startDate: '2026-05-24',
          endDate: '2026-06-23',
          dimensions: ['date'],
          rowLimit: 30,
        },
      });
      scOverall = overall.data;
      usedSiteUrl = siteUrl;

      const queries = await sc.searchanalytics.query({
        siteUrl,
        requestBody: {
          startDate: '2026-05-24',
          endDate: '2026-06-23',
          dimensions: ['query'],
          rowLimit: 25,
        },
      });
      scQueries = queries.data;

      const pages = await sc.searchanalytics.query({
        siteUrl,
        requestBody: {
          startDate: '2026-05-24',
          endDate: '2026-06-23',
          dimensions: ['page'],
          rowLimit: 10,
        },
      });
      scPages = pages.data;
      break;
    } catch (e) {
      console.error(`SC failed for ${siteUrl}: ${e.message}`);
    }
  }

  console.log(JSON.stringify({
    ga4: {
      daily: daily.data,
      prevPeriod: prevPeriod.data,
      sources: sources.data,
      landing: landing.data,
      newVsReturning: newVsReturning.data,
      events: events.data,
    },
    searchConsole: {
      usedSiteUrl,
      sites: scSites,
      overall: scOverall,
      queries: scQueries,
      pages: scPages,
    },
  }, null, 2));
}

main().catch(err => {
  console.error('FATAL:', err.message);
  if (err.response?.data) console.error(JSON.stringify(err.response.data, null, 2));
  process.exit(1);
});
