fetch('http://127.0.0.1:8080/api/update_correct_answer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        subject: '臨床生理學與病理學',
        year: '115-1',
        exam_id: 1,
        no: 5,
        new_answer: 'AD'
    })
}).then(r => r.json()).then(console.log);
