/**
 * YouTube Analytics OAuth2 fetcher.
 * Loads credentials from local gitignored scripts/credentials.json or environment variables.
 */
import { google } from 'googleapis';
import http from 'http';
import { exec } from 'child_process';
import { readFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const credPath = resolve(__dirname, './credentials.json');

let CLIENT_ID = process.env.YT_CLIENT_ID;
let CLIENT_SECRET = process.env.YT_CLIENT_SECRET;

if (existsSync(credPath)) {
  try {
    const creds = JSON.parse(readFileSync(credPath, 'utf8'));
    CLIENT_ID = CLIENT_ID || creds.client_id;
    CLIENT_SECRET = CLIENT_SECRET || creds.client_secret;
  } catch (e) {
    console.warn('Warning: Could not parse local credentials.json:', e.message);
  }
}

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error('\n❌ ERROR: YouTube OAuth Client ID or Client Secret not found.');
  console.error('Please configure them in scripts/credentials.json or set YT_CLIENT_ID and YT_CLIENT_SECRET env variables.\n');
  process.exit(1);
}

const REDIRECT_URI = 'http://localhost:8080/callback';
const oauth2Client = new google.auth.OAuth2(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI);

const SCOPES = [
  'https://www.googleapis.com/auth/youtube.readonly',
  'https://www.googleapis.com/auth/yt-analytics.readonly',
];

// ── Step 1: Auth URL ──────────────────────────────────────────────────────────
const authUrl = oauth2Client.generateAuthUrl({
  access_type: 'offline',
  scope: SCOPES,
  prompt: 'consent',
});

console.log('\n📺 Opening browser for YouTube auth...');
console.log('\nIf browser doesn\'t open, visit:\n', authUrl, '\n');
exec(`open "${authUrl}"`); // macOS

// ── Step 2: Local callback server ─────────────────────────────────────────────
const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost:8080');
  if (url.pathname !== '/callback') return;

  const code = url.searchParams.get('code');
  if (!code) {
    res.end('No code received.');
    server.close();
    return;
  }

  res.end('<html><body><h2>Auth complete. You can close this tab.</h2></body></html>');
  server.close();

  try {
    // ── Step 3: Exchange code for tokens ────────────────────────────────────
    const { tokens } = await oauth2Client.getToken(code);
    oauth2Client.setCredentials(tokens);

    const youtube = google.youtube({ version: 'v3', auth: oauth2Client });
    const youtubeAnalytics = google.youtubeAnalytics({ version: 'v2', auth: oauth2Client });

    // ── Get authenticated channel ─────────────────────────────────────────
    const channelRes = await youtube.channels.list({
      part: ['snippet', 'statistics', 'contentDetails'],
      mine: true,
    });
    const channel = channelRes.data.items?.[0];
    const channelId = channel?.id;
    console.log('\n✅ Channel:', channel?.snippet?.title, '|', channelId);
    console.log('   Subscribers:', channel?.statistics?.subscriberCount);
    console.log('   Total views:', channel?.statistics?.viewCount);
    console.log('   Videos:', channel?.statistics?.videoCount);

    // ── All uploaded videos ───────────────────────────────────────────────
    const uploadsPlaylistId = channel?.contentDetails?.relatedPlaylists?.uploads;
    let allVideoIds = [];
    if (uploadsPlaylistId) {
      const playlistRes = await youtube.playlistItems.list({
        part: ['snippet', 'contentDetails'],
        playlistId: uploadsPlaylistId,
        maxResults: 50,
      });
      allVideoIds = (playlistRes.data.items || []).map(i => i.contentDetails?.videoId).filter(Boolean);
    }

    // ── Video details (duration, title) ───────────────────────────────────
    let videoDetails = [];
    if (allVideoIds.length) {
      const vRes = await youtube.videos.list({
        part: ['snippet', 'contentDetails', 'statistics'],
        id: allVideoIds.join(','),
      });
      videoDetails = vRes.data.items || [];
    }

    // ── Analytics: channel-level last 30 days ────────────────────────────
    const endDate = new Date().toISOString().slice(0, 10);
    const startDate30 = new Date(Date.now() - 30 * 86400000).toISOString().slice(0, 10);
    const startDate90 = new Date(Date.now() - 90 * 86400000).toISOString().slice(0, 10);

    let channelAnalytics30 = null;
    let dailyAnalytics = null;
    let trafficSources = null;
    let videoAnalytics = null;

    if (channelId) {
      const ids = `channel==${channelId}`;

      // 30-day totals
      const a30 = await youtubeAnalytics.reports.query({
        ids,
        startDate: startDate30,
        endDate,
        metrics: 'views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost',
      });
      channelAnalytics30 = a30.data;

      // Daily views last 30 days
      const daily = await youtubeAnalytics.reports.query({
        ids,
        startDate: startDate30,
        endDate,
        dimensions: 'day',
        metrics: 'views,estimatedMinutesWatched',
        sort: 'day',
      });
      dailyAnalytics = daily.data;

      // Traffic sources
      const traffic = await youtubeAnalytics.reports.query({
        ids,
        startDate: startDate90,
        endDate,
        dimensions: 'insightTrafficSourceType',
        metrics: 'views',
        sort: '-views',
      });
      trafficSources = traffic.data;

      // Per-video analytics (last 90 days for enough data)
      if (allVideoIds.length) {
        const va = await youtubeAnalytics.reports.query({
          ids,
          startDate: startDate90,
          endDate,
          dimensions: 'video',
          metrics: 'views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage',
          sort: '-views',
          maxResults: 20,
          filters: `video==${allVideoIds.join(',')}`,
        });
        videoAnalytics = va.data;
      }
    }

    // ── Print all data ─────────────────────────────────────────────────────
    console.log('\n\n=== YOUTUBE DATA (copy this into mock-data.ts) ===\n');
    console.log(JSON.stringify({
      channel: {
        title: channel?.snippet?.title,
        id: channelId,
        subscribers: channel?.statistics?.subscriberCount,
        totalViews: channel?.statistics?.viewCount,
        videoCount: channel?.statistics?.videoCount,
      },
      analytics30: channelAnalytics30,
      daily: dailyAnalytics,
      trafficSources,
      videoDetails: videoDetails.map(v => ({
        id: v.id,
        title: v.snippet?.title,
        publishedAt: v.snippet?.publishedAt,
        duration: v.contentDetails?.duration,
        viewCount: v.statistics?.viewCount,
        likeCount: v.statistics?.likeCount,
        commentCount: v.statistics?.commentCount,
      })),
      videoAnalytics,
    }, null, 2));

  } catch (e) {
    console.error('ERROR:', e.message);
    if (e.response?.data) console.error(JSON.stringify(e.response.data, null, 2));
  }
});

server.listen(8080, () => {
  console.log('Waiting for OAuth callback on http://localhost:8080/callback ...');
});
