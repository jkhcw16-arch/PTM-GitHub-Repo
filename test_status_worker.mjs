import assert from "node:assert/strict"; import worker from "../src/index.js";
const env={ASSETS:{fetch:async()=>new Response("site")}};
let r=await worker.fetch(new Request("https://x/api/status"),env); assert.equal(r.status,200); assert.deepEqual(await r.json(),{project:"Pairwise Temporal Memory",version:"1.3.0",status:"candidate",ontology:"available",shacl:"available"});
r=await worker.fetch(new Request("https://x/api/release"),env); assert.equal(r.status,200); assert.deepEqual(await r.json(),{project:"Pairwise Temporal Memory",version:"1.3.0",status:"candidate",artifacts:{ontology:"ontology/ptm-1.3.0-additions.ttl",shacl:"ontology/ptm-1.3.0-additions.shacl.ttl"}});
r=await worker.fetch(new Request("https://x/api/release",{method:"POST"}),env); assert.equal(r.status,405);
console.log("PTM API tests: PASS");
