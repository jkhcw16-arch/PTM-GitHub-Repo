import release from "../release-manifest.json" with { type: "json" };
const status = Object.freeze({project:release.project,version:release.version,status:release.status,ontology:"available",shacl:"available"});
function jsonEndpoint(request, payload) {
  if (request.method !== "GET" && request.method !== "HEAD") return Response.json({error:"method_not_allowed"},{status:405,headers:{Allow:"GET, HEAD","X-Content-Type-Options":"nosniff"}});
  return Response.json(payload,{headers:{"Cache-Control":"public, max-age=60","X-Content-Type-Options":"nosniff"}});
}

const CONTACT_MAX_BODY = 12_000;
const CONTACT_FIELDS = { name: 120, organization: 160, email: 254, useCase: 1200, integrationInterest: 800, message: 4000 };
function clean(value, max) { return typeof value === "string" ? value.trim().slice(0, max) : ""; }
function validEmail(value) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) && value.length <= 254; }
async function verifyTurnstile(token, request, env) {
  if (!env.TURNSTILE_SECRET_KEY) return { success: false, configurationError: true };
  if (typeof token !== "string" || !token || token.length > 2048) return { success: false };
  const remoteip = request.headers.get("CF-Connecting-IP") || undefined;
  const idempotencyKey = crypto.randomUUID();
  const response = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ secret: env.TURNSTILE_SECRET_KEY, response: token, remoteip, idempotency_key: idempotencyKey })
  });
  if (!response.ok) return { success: false };
  return await response.json();
}
async function contactEndpoint(request, env) {
  if (request.method !== "POST") return Response.json({error:"method_not_allowed"},{status:405,headers:{Allow:"POST","X-Content-Type-Options":"nosniff"}});
  const type=(request.headers.get("content-type")||"").toLowerCase();
  if (!type.includes("application/json")) return Response.json({error:"unsupported_media_type"},{status:415});
  const declared=Number(request.headers.get("content-length")||0);
  if (declared > CONTACT_MAX_BODY) return Response.json({error:"payload_too_large"},{status:413});
  let body; try { body=await request.json(); } catch { return Response.json({error:"invalid_json"},{status:400}); }
  const data={}; for (const [key,max] of Object.entries(CONTACT_FIELDS)) data[key]=clean(body?.[key],max);
  const turnstile = await verifyTurnstile(body?.turnstileToken, request, env);
  if (turnstile.configurationError) return Response.json({error:"contact_service_unavailable"},{status:503});
  if (!turnstile.success) return Response.json({error:"turnstile_failed"},{status:403});
  if (!data.name || !data.email || !data.message) return Response.json({error:"missing_required_fields",required:["name","email","message"]},{status:400});
  if (!validEmail(data.email)) return Response.json({error:"invalid_email"},{status:400});
  if (!env.CONTACT_DB) return Response.json({error:"contact_service_unavailable"},{status:503});
  const id=crypto.randomUUID(); const createdAt=new Date().toISOString();
  await env.CONTACT_DB.prepare("INSERT INTO contact_inquiries (id, created_at, name, organization, email, use_case, integration_interest, message) VALUES (?1,?2,?3,?4,?5,?6,?7,?8)").bind(id,createdAt,data.name,data.organization,data.email,data.useCase,data.integrationInterest,data.message).run();
  return Response.json({accepted:true,reference:id},{status:202,headers:{"Cache-Control":"no-store","X-Content-Type-Options":"nosniff"}});
}
export default { async fetch(request, env) {
  const path=new URL(request.url).pathname;
  if(path==="/api/status") return jsonEndpoint(request,status);
  if(path==="/api/release") return jsonEndpoint(request,release);
  if(path==="/api/contact") return contactEndpoint(request,env);
  return env.ASSETS ? env.ASSETS.fetch(request) : new Response("Not Found",{status:404});
}};
