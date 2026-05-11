// -- Gantt --

function drawGantt(tasks, maxShow = 30) {
	const subset = tasks.slice(0, maxShow);
	const svg    = document.getElementById('gantt-svg');
	const W      = svg.parentElement.clientWidth - 40;
	const rowH   = 24, padL = 80, padR = 120;
	const H      = subset.length * rowH + 30;
	const maxT   = Math.max(...subset.map(t => Math.max(t.finish, t.deadline))) * 1.05;
	const scaleX = (W - padL - padR) / maxT;

	svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
	svg.setAttribute('height', H);

	let html = '';
	subset.forEach((t, i) => {
		const y    = i * rowH + 4;
		const x0   = padL + t.start * scaleX;
		const bw   = t.duration * scaleX;
		const dlX  = padL + t.deadline * scaleX;
		const color = t.isLate ? '#FF4560' : '#00E5A0';
		const alpha = t.isLate ? 'cc' : '99';

		html += `<text x="${padL - 6}" y="${y + 12}" fill="#5C6B80" font-size="9" font-family="JetBrains Mono" text-anchor="end">${t.name}</text>`;
		html += `<rect x="${x0}" y="${y}" width="${Math.max(bw, 1)}" height="${rowH - 5}" rx="3" fill="${color}${alpha}"/>`;
		html += `<line x1="${dlX}" y1="${y - 2}" x2="${dlX}" y2="${y + rowH - 3}" stroke="#555" stroke-width="1" stroke-dasharray="3,2"/>`;
		if (t.isLate) {
			html += `<text x="${padL + t.finish * scaleX + 4}" y="${y + 12}" fill="#FF4560" font-size="9" font-family="JetBrains Mono">⚠ +${t.lateness.toFixed(0)}s</text>`;
		}
	});

	// axis
	const tickCount = 8;
	for (let k = 0; k <= tickCount; k++) {
		const xT = padL + (k / tickCount) * (W - padL - padR);
		const tVal = ((k / tickCount) * maxT).toFixed(0);
		html += `<line x1="${xT}" y1="0" x2="${xT}" y2="${H - 20}" stroke="#1E2835" stroke-width="1"/>`;
		html += `<text x="${xT}" y="${H - 4}" fill="#5C6B80" font-size="9" font-family="JetBrains Mono" text-anchor="middle">${tVal}s</text>`;
	}

	svg.innerHTML = html;
}
