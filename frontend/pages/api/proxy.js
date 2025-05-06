export default async function handler(req, res) {
    const { latex } = await req.body;
  
    // 1. Submit to orchestrator
    const enq = await fetch('http://orchestrator:8000/enqueue', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ paper_id: 'demo', sections: { latex } })
    });
    const { job_id } = await enq.json();
  
    // 2. Poll until done
    let status;
    do {
      await new Promise(r => setTimeout(r, 1000));
      const st = await fetch(`http://orchestrator:8000/status/${job_id}`);
      status = await st.json();
    } while (status.status !== 'done');
  
    // 3. Send render request
    const videoRes = await fetch('http://renderer:8001/render', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(status.job_content)
    });
    const videoData = await videoRes.json();
  
    res.status(200).json({
      summary: status.summary,
      video_url: videoData.video_path
    });
  }
  