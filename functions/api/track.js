// Cloudflare Pages Function for /api/track on daohang.bot.cd
export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);

  if (request.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
      },
    });
  }

  const site = url.searchParams.get("s") || "daohang.bot.cd";
  const path = url.searchParams.get("p") || "/";
  const ref = url.searchParams.get("r") || "";
  const event = url.searchParams.get("e") || "pageview";
  const country = request.cf?.country || "XX";
  const city = request.cf?.city || "Unknown";
  const ip = request.headers.get("CF-Connecting-IP") || "0.0.0.0";
  const ua = request.headers.get("User-Agent") || "";
  const timestamp = new Date().toISOString();

  let source = "direct";
  const lowerRef = ref.toLowerCase();
  if (lowerRef.includes("chatgpt.com") || lowerRef.includes("android-app://com.openai.chatgpt")) source = "ai:chatgpt";
  else if (lowerRef.includes("perplexity.ai")) source = "ai:perplexity";
  else if (lowerRef.includes("claude.ai")) source = "ai:claude";
  else if (lowerRef.includes("copilot.microsoft.com")) source = "ai:copilot";
  else if (lowerRef.includes("google.")) source = "search:google";
  else if (lowerRef.includes("bing.")) source = "search:bing";
  else if (lowerRef.includes("baidu.")) source = "search:baidu";
  else if (lowerRef.includes("weixin.qq.com") || lowerRef.includes("mp.weixin")) source = "social:wechat";
  else if (lowerRef.includes("t.co") || lowerRef.includes("twitter.com") || lowerRef.includes("x.com")) source = "social:x";
  else if (ref) source = "referral:" + lowerRef.replace(/^https?:\/\//, "").split("/")[0];

  console.log(JSON.stringify({
    type: "TELEMETRY_LOG",
    timestamp,
    site,
    path,
    event,
    source,
    ref,
    country,
    city,
    ip,
    ua
  }));

  const gif = new Uint8Array([
    71, 73, 70, 56, 57, 97, 1, 0, 1, 0, 128, 0, 0, 255, 255, 255,
    0, 0, 0, 33, 249, 4, 1, 0, 0, 0, 0, 44, 0, 0, 0, 0,
    1, 0, 1, 0, 0, 2, 2, 68, 1, 0, 59
  ]);

  return new Response(gif, {
    headers: {
      "Content-Type": "image/gif",
      "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
